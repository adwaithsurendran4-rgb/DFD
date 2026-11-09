# DFD Platform — Interactive Data Flow Diagram Studio & DeepFake Forensics Lab

A full-stack web application built with **Django 6.0**, **Django REST Framework**, and **Pillow**, synthesizing standards, architectures, and open-source implementations from across the internet into a comprehensive platform.

---

## 🌟 Key Features

### 1. 📐 Interactive DFD Canvas Studio
- **Multi-Notation Support**:
  - **Gane & Sarson Notation**: Rounded rectangle processes with header bands, open-ended rectangles for data stores.
  - **Yourdon & DeMarco Notation**: Circular processes, parallel horizontal lines for data stores.
- **Hierarchical Diagram Levels**:
  - **Level 0 (Context Diagram)**: High-level system boundary, single system process (Process 0), external entities, boundary data flows.
  - **Level 1 (Decomposition Diagram)**: Functional explosion into sub-processes (1.0, 2.0, 3.0...), data stores (D1, D2...), and entity interactions.
  - **Level 2 (Detailed Diagram)**: Detailed drill-down into specific process sub-tasks.
- **Real-Time Software Engineering Rule Validator**:
  - Automatically flags **Miracle Processes** (outputs with zero inputs).
  - Detects **Black Hole Processes** (inputs with zero outputs).
  - Blocks illegal direct connections (Entity-to-Entity, DataStore-to-DataStore, Entity-to-DataStore).
  - Checks for orphan nodes and unlabeled flows with a real-time compliance score (0–100%).
- **Interactive Drag & Drop Canvas**:
  - Pan, zoom (40% to 200%), and grid alignment.
  - Draw curved directional Bezier arrows with editable flow labels.
  - Double-click to edit process numbers, labels, or descriptions.
- **Export & Import**:
  - High-Resolution **PNG** image export.
  - Scalable Vector Graphics (**SVG**) export.
  - **JSON** project file export and import.
  - Database persistence via SQLite & Django ORM.

---

### 2. 🌐 Internet Architecture Templates (15 Systems)
Pre-loaded with 15 complete, validated software engineering system architectures sourced from academic standards and internet specifications:
1. **Online Banking & ATM Transaction System** (Core banking, ledger, interbank switch)
2. **Hospital Management & Patient EHR System** (Outpatient triage, doctor consultation, pharmacy, billing)
3. **E-Commerce Shopping & Checkout System** (Catalog search, cart, payment gateway, courier tracking)
4. **College Student Management & Exam System** (Admissions, course electives, grade transcripts)
5. **Airline / Flight Reservation System** (Flight schedules, PNR bookings, web check-in, gate manifest)
6. **Hotel Room Booking & Hospitality System** (Room inventory, reservations, front desk folio, check-out)
7. **Online Food Delivery Platform** (Swiggy/DoorDash style menu browsing, kitchen routing, GPS driver dispatch)
8. **Digital Library Management System** (Catalog search, book loan circulation, overdue fines)
9. **Ride-Hailing & Taxi Dispatch System** (Uber style surge pricing, geospatial driver matching, trip telemetry)
10. **Social Media & Content Sharing Network** (Posts, friends graph, algorithmic feed generation, moderation)
11. **Warehouse Inventory & Supply Chain Logistics** (Inbound GRN, warehouse binning, wave picking, automated reordering)
12. **Payroll, Attendance & HR Management System** (Biometric clock-in, salary tax computation, direct deposit ACH)
13. **Online Examination & Automated Proctoring** (Question banks, timed test delivery, AI proctoring logs)
14. **Railway Ticket Booking & Train Tracking** (IRCTC style train quotas, PNR charting, TTE handheld manifest)
15. **Vehicle Rental & Fleet Management System** (Depot inventory, license verification, IoT digital key, security deposit)

---

### 3. 🧠 Smart AI / NLP DFD Generator
- Type any system requirement or user story in natural language.
- The built-in heuristic NLP engine extracts external entities (actors), core functional processes, and persistent data stores.
- Automatically generates and lays out both **Level 0** and **Level 1** diagrams with 1 click!

---

### 4. 📋 Software Engineering Data Dictionary (IEEE-Std 830)
- Auto-generates a structured Data Dictionary table for any diagram.
- Defines data flows, data structures, composition, process specifications, and data stores.
- Supports 1-click **Print / PDF** generation and **CSV export**.

---

### 5. 🛡️ DeepFake Detection (DFD) Forensics Lab
- Forensic media analysis for images uploaded locally or fetched via public internet URL:
  - **Error Level Analysis (ELA)**: Resaves at 90% JPEG quality to compute compression disparity heatmaps.
  - **Spatial Edge & Noise Variance**: Detects generative smoothing and boundary splicing seams.
  - **Metadata & EXIF Scanner**: Scans for AI signatures (Midjourney, DALL-E, Stable Diffusion, Photoshop) vs verified camera hardware.
  - **Deepfake Authenticity Score Meter**: 0–100% fake probability gauge with forensic summary.
  - **Interactive Split Comparison Slider**: Compare original frame side-by-side with the ELA heatmap.

---

## 🚀 How to Run the Application

From the project directory:
```bash
python manage.py runserver 127.0.0.1:8000
```
Then open your web browser at:
```
http://127.0.0.1:8000/
```

### Key URLs:
- **DFD Canvas Studio**: `http://127.0.0.1:8000/`
- **Internet Templates Gallery**: `http://127.0.0.1:8000/templates/`
- **DeepFake Detection Lab**: `http://127.0.0.1:8000/forensics/`
- **Software Engineering DFD Guide**: `http://127.0.0.1:8000/docs/`

"# DFD" 
