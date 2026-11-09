import uuid
from django.db import models


class Project(models.Model):
    NOTATION_CHOICES = [
        ('gane_sarson', 'Gane & Sarson (Rounded Rectangles & Open Rectangles)'),
        ('yourdon_demarco', 'Yourdon & DeMarco (Circles & Parallel Lines)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, default='Untitled DFD Project')
    description = models.TextField(blank=True, default='')
    notation_style = models.CharField(max_length=30, choices=NOTATION_CHOICES, default='gane_sarson')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Diagram(models.Model):
    LEVEL_CHOICES = [
        (0, 'Level 0 (Context Diagram)'),
        (1, 'Level 1 (Decomposition Diagram)'),
        (2, 'Level 2 (Detailed Sub-process Diagram)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='diagrams')
    level = models.IntegerField(choices=LEVEL_CHOICES, default=0)
    parent_process_id = models.CharField(max_length=100, blank=True, null=True, help_text="Process ID for Level 2 drill-down")
    name = models.CharField(max_length=200, default='Diagram')
    graph_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['level', 'created_at']

    def __str__(self):
        return f"{self.project.name} - Level {self.level}: {self.name}"


class DFDTemplate(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default='General')
    summary = models.TextField()
    description = models.TextField(blank=True)
    level0_data = models.JSONField(default=dict)
    level1_data = models.JSONField(default=dict)
    level2_data = models.JSONField(default=dict, blank=True)
    data_dictionary = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.category}] {self.title}"


class ForensicScan(models.Model):
    VERDICT_CHOICES = [
        ('authentic', 'Authentic / Real Media'),
        ('likely_real', 'Likely Authentic'),
        ('suspicious', 'Suspicious / Potential Manipulation'),
        ('deepfake', 'Manipulated / Deepfake Detected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default='Media Forensics Scan')
    source_type = models.CharField(max_length=20, default='upload')  # upload or url
    source_url = models.URLField(max_length=1000, blank=True, null=True)
    original_image = models.ImageField(upload_to='forensics/original/', blank=True, null=True)
    ela_image = models.ImageField(upload_to='forensics/ela/', blank=True, null=True)
    noise_image = models.ImageField(upload_to='forensics/noise/', blank=True, null=True)
    deepfake_score = models.FloatField(default=0.0)  # 0 to 100 percentage fake
    verdict = models.CharField(max_length=30, choices=VERDICT_CHOICES, default='likely_real')
    analysis_details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_verdict_display()} ({self.deepfake_score:.1f}%)"
