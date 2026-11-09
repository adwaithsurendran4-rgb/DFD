"""
DeepFake Detection (DFD) Forensics Engine:
Performs Error Level Analysis (ELA), Noise Discrepancy Scanning,
High-Frequency Artifact Detection, and EXIF/Metadata Forensics.
"""
import io
import os
import uuid
import requests
from PIL import Image, ImageChops, ImageEnhance, ImageFilter
from PIL.ExifTags import TAGS
from django.conf import settings


def run_error_level_analysis(original_pil_image, quality=90, scale=18):
    """
    Computes Error Level Analysis (ELA).
    Identifies areas of an image that have different compression levels,
    a hallmark of manipulated facial regions, deepfakes, and spliced imagery.
    """
    # Create in-memory JPEG resaved copy
    buffer = io.BytesIO()
    rgb_img = original_pil_image.convert('RGB')
    rgb_img.save(buffer, 'JPEG', quality=quality)
    buffer.seek(0)
    resaved_img = Image.open(buffer)

    # Compute difference
    diff = ImageChops.difference(rgb_img, resaved_img)

    # Calculate statistics from difference
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema]) if extrema else 1
    if max_diff == 0:
        max_diff = 1

    # Enhance brightness to make artifacts human-visible
    scale_multiplier = 255.0 / max_diff
    enhancer = ImageEnhance.Brightness(diff)
    ela_enhanced = enhancer.enhance(scale_multiplier * 0.75)

    # Calculate mean error score across pixels
    grayscale_diff = diff.convert('L')
    pixels = list(grayscale_diff.getdata())
    mean_diff = sum(pixels) / len(pixels) if pixels else 0

    return ela_enhanced, mean_diff


def run_noise_and_edge_analysis(original_pil_image):
    """
    Computes high-frequency edge gradients to detect blending seams,
    warping, or generative smoothing artifacts.
    """
    rgb_img = original_pil_image.convert('RGB')
    edges = rgb_img.filter(ImageFilter.FIND_EDGES)
    enhancer = ImageEnhance.Color(edges)
    edges_colored = enhancer.enhance(2.0)

    # Metric: variance of edges
    gray_edges = edges.convert('L')
    pixels = list(gray_edges.getdata())
    mean_edge = sum(pixels) / len(pixels) if pixels else 0
    variance_edge = sum((p - mean_edge) ** 2 for p in pixels) / len(pixels) if pixels else 0

    return edges_colored, mean_edge, variance_edge


def extract_metadata_and_exif(original_pil_image):
    """
    Extracts EXIF and checks for known AI generation patterns and editing tools.
    """
    exif_data = {}
    ai_signatures_found = []
    has_camera_hardware = False

    try:
        raw_exif = original_pil_image.getexif()
        if raw_exif:
            for tag_id, value in raw_exif.items():
                tag_name = TAGS.get(tag_id, str(tag_id))
                val_str = str(value).strip()
                exif_data[tag_name] = val_str

                # Check camera hardware tags
                if tag_name in ['Make', 'Model', 'LensModel', 'FNumber', 'ExposureTime']:
                    has_camera_hardware = True

                # Check for AI / Software signatures
                val_lower = val_str.lower()
                for tool in ['midjourney', 'stable diffusion', 'dall-e', 'photoshop', 'deepface', 'gimp', 'novelai', 'firefly', 'canva']:
                    if tool in val_lower:
                        ai_signatures_found.append(f"Metadata tag '{tag_name}' references: {tool.title()}")
    except Exception:
        pass

    # Check image info dictionary
    for k, v in original_pil_image.info.items():
        v_str = str(v).lower()
        for tool in ['midjourney', 'stable diffusion', 'dall-e', 'photoshop', 'deepfake', 'automatic1111']:
            if tool in v_str and tool not in [s.lower() for s in ai_signatures_found]:
                ai_signatures_found.append(f"Image chunk '{k}' contains '{tool.title()}'")

    return exif_data, ai_signatures_found, has_camera_hardware


def analyze_media_forensics(input_source, is_url=False):
    """
    Full Forensic Pipeline:
    - Loads media from file or internet URL
    - Executes ELA and Edge analysis
    - Computes deepfake/tampering confidence score
    - Saves output artifacts into Django media directory
    """
    if is_url:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) DFD-ForensicScanner/1.0'}
        response = requests.get(input_source, headers=headers, timeout=12)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
        original_filename = "url_download_" + uuid.uuid4().hex[:8] + ".jpg"
    else:
        img = Image.open(input_source)
        original_filename = getattr(input_source, 'name', 'upload_' + uuid.uuid4().hex[:8] + '.jpg')

    # Convert image format
    img_rgb = img.convert('RGB')

    # Ensure output media directories exist
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'forensics', 'original'), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'forensics', 'ela'), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'forensics', 'noise'), exist_ok=True)

    file_stem = uuid.uuid4().hex
    orig_path = os.path.join(settings.MEDIA_ROOT, 'forensics', 'original', f"{file_stem}_orig.jpg")
    ela_path = os.path.join(settings.MEDIA_ROOT, 'forensics', 'ela', f"{file_stem}_ela.jpg")
    noise_path = os.path.join(settings.MEDIA_ROOT, 'forensics', 'noise', f"{file_stem}_noise.jpg")

    # Save original
    img_rgb.save(orig_path, 'JPEG', quality=95)

    # 1. Error Level Analysis (ELA)
    ela_image, mean_ela = run_error_level_analysis(img_rgb)
    ela_image.save(ela_path, 'JPEG', quality=95)

    # 2. Noise & Edge Analysis
    edge_image, mean_edge, var_edge = run_noise_and_edge_analysis(img_rgb)
    edge_image.save(noise_path, 'JPEG', quality=95)

    # 3. Metadata analysis
    exif_tags, ai_flags, has_camera = extract_metadata_and_exif(img)

    # 4. Scoring Algorithm (0 - 100% manipulation likelihood)
    score = 0.0

    # ELA factor (normalized mean difference)
    # Natural photos usually have mean_ela in 3.0 - 7.0 range.
    # Higher or abnormally low values indicate tampering / GAN synthesis.
    if mean_ela > 12.0:
        score += 35.0
    elif mean_ela > 8.0:
        score += 22.0
    elif mean_ela < 2.2:
        # Extremely flat compression often seen in AI-generated images
        score += 28.0
    else:
        score += 10.0

    # Edge and high-frequency factor
    if var_edge < 120.0:
        # Unusually smooth skin texture, lack of sensor grain (common in deepfake face-swaps)
        score += 25.0
    elif var_edge > 1200.0:
        # High frequency noise borders / splicing artifacts
        score += 20.0
    else:
        score += 8.0

    # Metadata factor
    if ai_flags:
        score += 40.0
    elif not has_camera:
        # Web media stripped of camera hardware tags
        score += 15.0

    # Clamp score
    deepfake_score = min(98.5, max(4.0, score))

    if deepfake_score >= 70.0:
        verdict = 'deepfake'
        verdict_label = 'Manipulated / Deepfake Detected'
        summary_verdict = 'Significant compression disparity and synthetic noise patterns detected. High probability of deepfake or generative AI origin.'
    elif deepfake_score >= 45.0:
        verdict = 'suspicious'
        verdict_label = 'Suspicious / Potential Manipulation'
        summary_verdict = 'Moderate inconsistencies observed in error level analysis and frequency layers. Manual forensic review recommended.'
    elif deepfake_score >= 25.0:
        verdict = 'likely_real'
        verdict_label = 'Likely Authentic'
        summary_verdict = 'Minor compression variations consistent with standard internet re-encoding. No direct tampering signatures found.'
    else:
        verdict = 'authentic'
        verdict_label = 'Authentic / Real Media'
        summary_verdict = 'Uniform error distribution and natural camera sensor characteristics. Image appears genuine.'

    return {
        'deepfake_score': round(deepfake_score, 1),
        'verdict': verdict,
        'verdict_label': verdict_label,
        'summary': summary_verdict,
        'mean_ela': round(mean_ela, 2),
        'edge_variance': round(var_edge, 1),
        'has_camera_hardware': has_camera,
        'ai_signatures': ai_flags,
        'exif_summary': {k: str(v)[:80] for k, v in list(exif_tags.items())[:12]},
        'orig_url': f"{settings.MEDIA_URL}forensics/original/{file_stem}_orig.jpg",
        'ela_url': f"{settings.MEDIA_URL}forensics/ela/{file_stem}_ela.jpg",
        'noise_url': f"{settings.MEDIA_URL}forensics/noise/{file_stem}_noise.jpg",
        'dimensions': f"{img.width} x {img.height} px"
    }

