"""
Internet DFD Templates Repository:
15 Complete, production-grade Software Engineering Data Flow Diagrams
compiled from academic standards, IEEE software specifications, and industry internet architectures.
"""

INTERNET_TEMPLATES = [
    {
        "slug": "online-banking-atm",
        "title": "Online Banking & ATM Transaction System",
        "category": "Banking & Finance",
        "summary": "Core banking data flow covering cash withdrawals, deposits, fund transfers, and balance inquiries across ATM kiosks and mobile apps.",
        "description": "Standard banking DFD mapping customer PIN authentication, account verification, ledger updates, transaction logging, and interbank settlement network integration (NPCI / VISA / Mastercard).",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Online Banking & ATM System", "x": 520, "y": 280, "width": 240, "height": 110, "description": "Automated Core Banking Engine"},
                {"id": "ent_1", "type": "entity", "label": "Bank Customer / Cardholder", "x": 120, "y": 280, "width": 180, "height": 80},
                {"id": "ent_2", "type": "entity", "label": "Bank Branch Officer / Manager", "x": 520, "y": 70, "width": 200, "height": 80},
                {"id": "ent_3", "type": "entity", "label": "Interbank Switch / Network", "x": 920, "y": 280, "width": 180, "height": 80},
                {"id": "ent_4", "type": "entity", "label": "SMS / Notification Gateway", "x": 520, "y": 490, "width": 180, "height": 80}
            ],
            "edges": [
                {"id": "e_b0_1", "source": "ent_1", "target": "proc_0", "label": "PIN, Card Details, Withdrawal/Transfer Request"},
                {"id": "e_b0_2", "source": "proc_0", "target": "ent_1", "label": "Dispense Cash, Transaction Receipt, Balance Slip"},
                {"id": "e_b0_3", "source": "ent_2", "target": "proc_0", "label": "Cash Load Auth, Audit Commands, Account Overrides"},
                {"id": "e_b0_4", "source": "proc_0", "target": "ent_2", "label": "Daily Settlement Reports, Cash Low Alerts"},
                {"id": "e_b0_5", "source": "proc_0", "target": "ent_3", "label": "Interbank Clearance Request, ISO 8583 Packet"},
                {"id": "e_b0_6", "source": "ent_3", "target": "proc_0", "label": "Interbank Authorization & Approval Code"},
                {"id": "e_b0_7", "source": "proc_0", "target": "ent_4", "label": "OTP & Instant Debit/Credit Alert Details"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_cust", "type": "entity", "label": "Bank Customer", "x": 80, "y": 260, "width": 160, "height": 80},
                {"id": "ent_switch", "type": "entity", "label": "Interbank Gateway", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "ent_admin", "type": "entity", "label": "Branch Auditor", "x": 1050, "y": 460, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Card & PIN Verification", "x": 380, "y": 100, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Account Balance & Limit Check", "x": 380, "y": 240, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Execute Fund Debit / Credit", "x": 380, "y": 380, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Generate Receipt & Audit Log", "x": 380, "y": 520, "width": 220, "height": 75},
                {"id": "ds_accounts", "type": "datastore", "number": "D1", "label": "Accounts & Customer Store", "x": 720, "y": 140, "width": 220, "height": 60},
                {"id": "ds_ledger", "type": "datastore", "number": "D2", "label": "General Ledger & Balance", "x": 720, "y": 320, "width": 220, "height": 60},
                {"id": "ds_txlogs", "type": "datastore", "number": "D3", "label": "Audit & Transaction Logs", "x": 720, "y": 500, "width": 220, "height": 60}
            ],
            "edges": [
                {"id": "eb1_1", "source": "ent_cust", "target": "proc_1_0", "label": "Card Track Data + Encrypted PIN"},
                {"id": "eb1_2", "source": "ds_accounts", "target": "proc_1_0", "label": "Stored PIN Hash & Card Status"},
                {"id": "eb1_3", "source": "proc_1_0", "target": "proc_2_0", "label": "Authenticated Session Token"},
                {"id": "eb1_4", "source": "ent_cust", "target": "proc_2_0", "label": "Requested Withdrawal Amount"},
                {"id": "eb1_5", "source": "ds_ledger", "target": "proc_2_0", "label": "Available Cleared Balance"},
                {"id": "eb1_6", "source": "proc_2_0", "target": "proc_3_0", "label": "Approved Amount Payload"},
                {"id": "eb1_7", "source": "proc_3_0", "target": "ds_ledger", "label": "Post Debit Transaction"},
                {"id": "eb1_8", "source": "proc_3_0", "target": "ent_switch", "label": "External Interbank Clearing"},
                {"id": "eb1_9", "source": "ent_switch", "target": "proc_3_0", "label": "Interbank Authorization Ack"},
                {"id": "eb1_10", "source": "proc_3_0", "target": "proc_4_0", "label": "Transaction Success Details"},
                {"id": "eb1_11", "source": "proc_4_0", "target": "ent_cust", "label": "Cash Dispense + Printed Receipt"},
                {"id": "eb1_12", "source": "proc_4_0", "target": "ds_txlogs", "label": "Write Timestamped Audit Record"},
                {"id": "eb1_13", "source": "ds_txlogs", "target": "ent_admin", "label": "Daily Balance Sheet & Audit Trail"}
            ]
        }
    },
    {
        "slug": "hospital-management-system",
        "title": "Hospital Management & Patient EHR System",
        "category": "Healthcare",
        "summary": "Hospital workflow diagram detailing patient outpatient/inpatient admission, doctor appointments, diagnosis, prescription, lab diagnostics, and billing.",
        "description": "Comprehensive healthcare DFD connecting patients, doctors, pharmacy dispensers, lab technicians, and insurance settlement agencies.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Hospital Management System", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_patient", "type": "entity", "label": "Patient", "x": 120, "y": 280, "width": 160, "height": 80},
                {"id": "ent_doctor", "type": "entity", "label": "Consulting Doctor", "x": 520, "y": 70, "width": 180, "height": 80},
                {"id": "ent_pharmacy", "type": "entity", "label": "Hospital Pharmacy", "x": 920, "y": 280, "width": 180, "height": 80},
                {"id": "ent_insurance", "type": "entity", "label": "Health Insurance Agency", "x": 520, "y": 490, "width": 190, "height": 80}
            ],
            "edges": [
                {"id": "eh0_1", "source": "ent_patient", "target": "proc_0", "label": "Demographic Details, Symptoms, Appointment Request"},
                {"id": "eh0_2", "source": "proc_0", "target": "ent_patient", "label": "Appointment Schedule, Medical Report, Discharge Bill"},
                {"id": "eh0_3", "source": "ent_doctor", "target": "proc_0", "label": "Clinical Notes, Prescriptions, Lab Test Orders"},
                {"id": "eh0_4", "source": "proc_0", "target": "ent_doctor", "label": "Patient Medical History, Lab Test Findings"},
                {"id": "eh0_5", "source": "proc_0", "target": "ent_pharmacy", "label": "Digital Drug Prescription Orders"},
                {"id": "eh0_6", "source": "ent_pharmacy", "target": "proc_0", "label": "Medication Dispense Status & Drug Bill"},
                {"id": "eh0_7", "source": "proc_0", "target": "ent_insurance", "label": "Cashless TPA Claim Submission & Diagnoses"},
                {"id": "eh0_8", "source": "ent_insurance", "target": "proc_0", "label": "Claim Authorization Code & Settlement"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_pat", "type": "entity", "label": "Patient", "x": 80, "y": 220, "width": 160, "height": 80},
                {"id": "ent_doc", "type": "entity", "label": "Doctor", "x": 80, "y": 450, "width": 160, "height": 80},
                {"id": "ent_pharm", "type": "entity", "label": "Pharmacy", "x": 1050, "y": 220, "width": 160, "height": 80},
                {"id": "ent_ins", "type": "entity", "label": "Insurance Agency", "x": 1050, "y": 450, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Patient Registration & Triage", "x": 380, "y": 100, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Doctor Consultation & EHR", "x": 380, "y": 240, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Pharmacy & Lab Ordering", "x": 380, "y": 380, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Invoicing & Claim Billing", "x": 380, "y": 520, "width": 220, "height": 75},
                {"id": "ds_pat_records", "type": "datastore", "number": "D1", "label": "Patient Master EHR Store", "x": 720, "y": 140, "width": 220, "height": 60},
                {"id": "ds_clinical", "type": "datastore", "number": "D2", "label": "Diagnostic & Prescription Log", "x": 720, "y": 320, "width": 220, "height": 60},
                {"id": "ds_billing", "type": "datastore", "number": "D3", "label": "Hospital Ledger & Invoices", "x": 720, "y": 500, "width": 220, "height": 60}
            ],
            "edges": [
                {"id": "eh1_1", "source": "ent_pat", "target": "proc_1_0", "label": "Registration & Insurance Info"},
                {"id": "eh1_2", "source": "proc_1_0", "target": "ds_pat_records", "label": "Save Patient Profile"},
                {"id": "eh1_3", "source": "ds_pat_records", "target": "proc_2_0", "label": "Retrieve Medical History"},
                {"id": "eh1_4", "source": "ent_doc", "target": "proc_2_0", "label": "Record Diagnosis & Rx"},
                {"id": "eh1_5", "source": "proc_2_0", "target": "ds_clinical", "label": "Save Treatment Plan"},
                {"id": "eh1_6", "source": "ds_clinical", "target": "proc_3_0", "label": "Active Prescriptions List"},
                {"id": "eh1_7", "source": "proc_3_0", "target": "ent_pharm", "label": "Prescription Order Dispatch"},
                {"id": "eh1_8", "source": "ent_pharm", "target": "proc_4_0", "label": "Dispense Charges & Cost"},
                {"id": "eh1_9", "source": "proc_4_0", "target": "ent_ins", "label": "Electronic Medical Claim Form"},
                {"id": "eh1_10", "source": "ent_ins", "target": "proc_4_0", "label": "Approved Insurance Coverage"},
                {"id": "eh1_11", "source": "proc_4_0", "target": "ds_billing", "label": "Store Final Consolidated Bill"},
                {"id": "eh1_12", "source": "proc_4_0", "target": "ent_pat", "label": "Patient Copay Bill & Discharge Slip"}
            ]
        }
    },
    {
        "slug": "ecommerce-shopping-system",
        "title": "E-Commerce Shopping & Checkout System",
        "category": "E-Commerce & Retail",
        "summary": "Full retail lifecycle diagram for browsing items, cart management, payment gateway integration, order fulfillment, and courier tracking.",
        "description": "Multi-tier commercial web application DFD modeling the customer purchasing journey, merchant inventory replenishment, and warehouse shipping.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "E-Commerce Web Platform", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_cust", "type": "entity", "label": "Online Shopper", "x": 120, "y": 280, "width": 160, "height": 80},
                {"id": "ent_merchant", "type": "entity", "label": "Seller / Merchant", "x": 520, "y": 70, "width": 180, "height": 80},
                {"id": "ent_courier", "type": "entity", "label": "Logistics & Delivery Partner", "x": 920, "y": 280, "width": 200, "height": 80},
                {"id": "ent_gateway", "type": "entity", "label": "Payment Gateway (Stripe/PayPal)", "x": 520, "y": 490, "width": 220, "height": 80}
            ],
            "edges": [
                {"id": "ec0_1", "source": "ent_cust", "target": "proc_0", "label": "Product Search, Cart Items, Delivery Address, Card Details"},
                {"id": "ec0_2", "source": "proc_0", "target": "ent_cust", "label": "Catalog Results, Order Invoice, Live Tracking Updates"},
                {"id": "ec0_3", "source": "ent_merchant", "target": "proc_0", "label": "Product Listings, Inventory Levels, Dispatch Handover"},
                {"id": "ec0_4", "source": "proc_0", "target": "ent_merchant", "label": "Order Alerts, Seller Payout Reports"},
                {"id": "ec0_5", "source": "proc_0", "target": "ent_courier", "label": "Waybill Manifest, Package Dimensions, Drop Address"},
                {"id": "ec0_6", "source": "ent_courier", "target": "proc_0", "label": "Tracking Milestones, Proof of Delivery (POD)"},
                {"id": "ec0_7", "source": "proc_0", "target": "ent_gateway", "label": "Authorization Payload, Cart Total"},
                {"id": "ec0_8", "source": "ent_gateway", "target": "proc_0", "label": "Payment Token & Charge Confirmation"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_c", "type": "entity", "label": "Shopper", "x": 80, "y": 220, "width": 150, "height": 80},
                {"id": "ent_m", "type": "entity", "label": "Merchant", "x": 80, "y": 440, "width": 150, "height": 80},
                {"id": "ent_pg", "type": "entity", "label": "Payment Gateway", "x": 1050, "y": 220, "width": 160, "height": 80},
                {"id": "ent_lg", "type": "entity", "label": "Logistics Partner", "x": 1050, "y": 440, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Browse & Product Catalog Search", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Shopping Cart & Price Calculation", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Order Placement & Payment Checkout", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Fulfillment & Dispatch Coordination", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_products", "type": "datastore", "number": "D1", "label": "Product Catalog & Stock", "x": 720, "y": 130, "width": 210, "height": 60},
                {"id": "ds_orders", "type": "datastore", "number": "D2", "label": "Customer Orders Store", "x": 720, "y": 310, "width": 210, "height": 60},
                {"id": "ds_shipments", "type": "datastore", "number": "D3", "label": "Shipments & Tracking Store", "x": 720, "y": 490, "width": 210, "height": 60}
            ],
            "edges": [
                {"id": "ec1_1", "source": "ent_c", "target": "proc_1_0", "label": "Search Keyword & Category Filter"},
                {"id": "ec1_2", "source": "ds_products", "target": "proc_1_0", "label": "Available Inventory & Prices"},
                {"id": "ec1_3", "source": "proc_1_0", "target": "ent_c", "label": "Filtered Product List"},
                {"id": "ec1_4", "source": "ent_c", "target": "proc_2_0", "label": "Add Item / Update Quantity"},
                {"id": "ec1_5", "source": "proc_2_0", "target": "proc_3_0", "label": "Validated Cart Subtotal + Taxes"},
                {"id": "ec1_6", "source": "proc_3_0", "target": "ent_pg", "label": "Customer Charge Amount"},
                {"id": "ec1_7", "source": "ent_pg", "target": "proc_3_0", "label": "Authorization Response"},
                {"id": "ec1_8", "source": "proc_3_0", "target": "ds_orders", "label": "Save Confirmed Order"},
                {"id": "ec1_9", "source": "proc_3_0", "target": "ds_products", "label": "Deduct Reserved Stock Quantity"},
                {"id": "ec1_10", "source": "ds_orders", "target": "proc_4_0", "label": "Ready to Ship Order Items"},
                {"id": "ec1_11", "source": "proc_4_0", "target": "ent_lg", "label": "Shipping Label & Consignment"},
                {"id": "ec1_12", "source": "ent_lg", "target": "proc_4_0", "label": "AWB Tracking Number"},
                {"id": "ec1_13", "source": "proc_4_0", "target": "ds_shipments", "label": "Record Shipment Status"},
                {"id": "ec1_14", "source": "ent_m", "target": "ds_products", "label": "Upload New Product Listings"}
            ]
        }
    },
    {
        "slug": "college-student-management",
        "title": "College Student Information & Examination System",
        "category": "Education & Academic",
        "summary": "University academic system capturing student enrollment, course registration, semester attendance, exam grading, and transcript generation.",
        "description": "Essential academic engineering DFD mapping students, faculty instructors, department chairs, and the university controller of examinations.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "College Student & Exam Portal", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_student", "type": "entity", "label": "College Student", "x": 120, "y": 280, "width": 160, "height": 80},
                {"id": "ent_faculty", "type": "entity", "label": "Course Instructor / Faculty", "x": 520, "y": 70, "width": 200, "height": 80},
                {"id": "ent_exam_cell", "type": "entity", "label": "Controller of Examinations", "x": 920, "y": 280, "width": 200, "height": 80},
                {"id": "ent_admin", "type": "entity", "label": "Academic Registrar", "x": 520, "y": 490, "width": 180, "height": 80}
            ],
            "edges": [
                {"id": "ecl0_1", "source": "ent_student", "target": "proc_0", "label": "Admission Application, Course Electives, Exam Fee"},
                {"id": "ecl0_2", "source": "proc_0", "target": "ent_student", "label": "Hall Ticket, Timetable, Grade Sheet / Transcript"},
                {"id": "ecl0_3", "source": "ent_faculty", "target": "proc_0", "label": "Attendance Logs, Internal Marks, Assignment Grades"},
                {"id": "ecl0_4", "source": "proc_0", "target": "ent_faculty", "label": "Class Student Roster, Course Syllabus Schedule"},
                {"id": "ecl0_5", "source": "ent_exam_cell", "target": "proc_0", "label": "Exam Datesheet, Moderated Marks, Grade Boundaries"},
                {"id": "ecl0_6", "source": "proc_0", "target": "ent_exam_cell", "label": "Student Eligibility List, Consolidated GPA Master"},
                {"id": "ecl0_7", "source": "ent_admin", "target": "proc_0", "label": "Degree Requirements, Department Quotas"},
                {"id": "ecl0_8", "source": "proc_0", "target": "ent_admin", "label": "Enrollment Statistics & Graduation List"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_s", "type": "entity", "label": "Student", "x": 80, "y": 220, "width": 150, "height": 80},
                {"id": "ent_f", "type": "entity", "label": "Faculty", "x": 80, "y": 440, "width": 150, "height": 80},
                {"id": "ent_ec", "type": "entity", "label": "Exam Controller", "x": 1050, "y": 220, "width": 160, "height": 80},
                {"id": "ent_reg", "type": "entity", "label": "Registrar", "x": 1050, "y": 440, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Admission & Student Onboarding", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Course Electives Registration", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Attendance & Internal Assessment", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Semester Exam & GPA Evaluation", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_students", "type": "datastore", "number": "D1", "label": "Student Master Database", "x": 720, "y": 130, "width": 210, "height": 60},
                {"id": "ds_courses", "type": "datastore", "number": "D2", "label": "Course Curriculum & Batches", "x": 720, "y": 310, "width": 210, "height": 60},
                {"id": "ds_grades", "type": "datastore", "number": "D3", "label": "Grades & Assessment Store", "x": 720, "y": 490, "width": 210, "height": 60}
            ],
            "edges": [
                {"id": "ecl1_1", "source": "ent_s", "target": "proc_1_0", "label": "Student Registration Details"},
                {"id": "ecl1_2", "source": "proc_1_0", "target": "ds_students", "label": "Assign Roll No & Store Bio"},
                {"id": "ecl1_3", "source": "ds_courses", "target": "proc_2_0", "label": "Available Course Sections"},
                {"id": "ecl1_4", "source": "ent_s", "target": "proc_2_0", "label": "Elective Preferences Selection"},
                {"id": "ecl1_5", "source": "proc_2_0", "target": "ds_students", "label": "Update Enrolled Subjects"},
                {"id": "ecl1_6", "source": "ent_f", "target": "proc_3_0", "label": "Daily Lecture Attendance Logs"},
                {"id": "ecl1_7", "source": "proc_3_0", "target": "ds_grades", "label": "Write Internal Test Scores"},
                {"id": "ecl1_8", "source": "ds_grades", "target": "proc_4_0", "label": "Aggregate Session Marks"},
                {"id": "ecl1_9", "source": "ent_ec", "target": "proc_4_0", "label": "End-Semester Theory Marks"},
                {"id": "ecl1_10", "source": "proc_4_0", "target": "ds_grades", "label": "Compute SGPA / CGPA Final"},
                {"id": "ecl1_11", "source": "proc_4_0", "target": "ent_s", "label": "Publish Verified Grade Card"},
                {"id": "ecl1_12", "source": "proc_4_0", "target": "ent_reg", "label": "Graduation Eligibility Report"}
            ]
        }
    },
    {
        "slug": "airline-flight-reservation",
        "title": "Airline / Flight Reservation System",
        "category": "Travel & Transportation",
        "summary": "Global Distribution System (GDS) and airline reservation flow covering flight search, seat allocation, boarding pass issuance, and baggage check-in.",
        "description": "Enterprise airline operations DFD handling passengers, travel agents, payment gateways, and airport boarding gate scanners.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Airline Flight Reservation System", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_passenger", "type": "entity", "label": "Airline Passenger", "x": 120, "y": 280, "width": 160, "height": 80},
                {"id": "ent_agent", "type": "entity", "label": "Travel Agent (OTA)", "x": 520, "y": 70, "width": 180, "height": 80},
                {"id": "ent_airport", "type": "entity", "label": "Airport Departure Control (DCS)", "x": 920, "y": 280, "width": 200, "height": 80},
                {"id": "ent_payment", "type": "entity", "label": "Payment Gateway", "x": 520, "y": 490, "width": 180, "height": 80}
            ],
            "edges": [
                {"id": "ea0_1", "source": "ent_passenger", "target": "proc_0", "label": "Origin/Destination, Flight Dates, Seat Choice"},
                {"id": "ea0_2", "source": "proc_0", "target": "ent_passenger", "label": "E-Ticket (PNR), Boarding Pass QR, Gate Info"},
                {"id": "ea0_3", "source": "ent_agent", "target": "proc_0", "label": "Bulk Seat Queries, GDS XML Flight Booking"},
                {"id": "ea0_4", "source": "proc_0", "target": "ent_agent", "label": "Confirmed PNRs, Commission Invoices"},
                {"id": "ea0_5", "source": "proc_0", "target": "ent_airport", "label": "Passenger Name Record (PNR) Manifest"},
                {"id": "ea0_6", "source": "ent_airport", "target": "proc_0", "label": "Boarded Passenger Scans & Bag Tag Status"},
                {"id": "ea0_7", "source": "proc_0", "target": "ent_payment", "label": "Fare Calculation & Card Charge Payload"},
                {"id": "ea0_8", "source": "ent_payment", "target": "proc_0", "label": "Payment Authorization & Transaction Code"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_pax", "type": "entity", "label": "Passenger", "x": 80, "y": 240, "width": 150, "height": 80},
                {"id": "ent_dcs", "type": "entity", "label": "Airport DCS", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Flight Schedule & Inventory Search", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Seat Allocation & Booking Request", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Payment Processing & Ticket Issue", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Web Check-In & Boarding Pass", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_flights", "type": "datastore", "number": "D1", "label": "Flight Schedules & Aircraft", "x": 720, "y": 130, "width": 210, "height": 60},
                {"id": "ds_reservations", "type": "datastore", "number": "D2", "label": "PNR & Bookings Store", "x": 720, "y": 310, "width": 210, "height": 60},
                {"id": "ds_manifest", "type": "datastore", "number": "D3", "label": "Flight Passenger Manifest", "x": 720, "y": 490, "width": 210, "height": 60}
            ],
            "edges": [
                {"id": "ea1_1", "source": "ent_pax", "target": "proc_1_0", "label": "Search Routes & Travel Date"},
                {"id": "ea1_2", "source": "ds_flights", "target": "proc_1_0", "label": "Available Flights & Cabin Seats"},
                {"id": "ea1_3", "source": "proc_1_0", "target": "ent_pax", "label": "Flight Itinerary Options"},
                {"id": "ea1_4", "source": "ent_pax", "target": "proc_2_0", "label": "Passenger Passport & Seat Choice"},
                {"id": "ea1_5", "source": "proc_2_0", "target": "ds_reservations", "label": "Create Tentative Booking Record"},
                {"id": "ea1_6", "source": "proc_2_0", "target": "proc_3_0", "label": "Pending PNR Reference"},
                {"id": "ea1_7", "source": "proc_3_0", "target": "ds_reservations", "label": "Confirm PNR with Payment Stamp"},
                {"id": "ea1_8", "source": "proc_3_0", "target": "ent_pax", "label": "Send Confirmed E-Ticket"},
                {"id": "ea1_9", "source": "ent_pax", "target": "proc_4_0", "label": "Check-In Request (PNR + Surname)"},
                {"id": "ea1_10", "source": "ds_reservations", "target": "proc_4_0", "label": "Verify Booking Status"},
                {"id": "ea1_11", "source": "proc_4_0", "target": "ds_manifest", "label": "Add Passenger to Gate Manifest"},
                {"id": "ea1_12", "source": "proc_4_0", "target": "ent_pax", "label": "Generate Printable Boarding Pass"},
                {"id": "ea1_13", "source": "ds_manifest", "target": "ent_dcs", "label": "Transmit Final Load Sheet"}
            ]
        }
    },
    {
        "slug": "hotel-management-system",
        "title": "Hotel Room Booking & Hospitality Management",
        "category": "Hospitality & Leisure",
        "summary": "Covers hotel room search, online reservation, front desk check-in/check-out, housekeeping status, room service billing, and final folio invoice.",
        "description": "Standard PMS (Property Management System) DFD mapping guests, receptionist, room service staff, and corporate accounts.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Hotel Management System", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_guest", "type": "entity", "label": "Hotel Guest", "x": 120, "y": 280, "width": 160, "height": 80},
                {"id": "ent_reception", "type": "entity", "label": "Front Desk Receptionist", "x": 520, "y": 70, "width": 200, "height": 80},
                {"id": "ent_housekeeping", "type": "entity", "label": "Housekeeping & Room Service", "x": 920, "y": 280, "width": 210, "height": 80},
                {"id": "ent_accountant", "type": "entity", "label": "Hotel Accounts & Auditor", "x": 520, "y": 490, "width": 190, "height": 80}
            ],
            "edges": [
                {"id": "eh0_1", "source": "ent_guest", "target": "proc_0", "label": "Booking Dates, Room Category, ID Proof, Advance Payment"},
                {"id": "eh0_2", "source": "proc_0", "target": "ent_guest", "label": "Reservation Voucher, Keycard Access, Final Bill Folio"},
                {"id": "eh0_3", "source": "ent_reception", "target": "proc_0", "label": "Walk-in Bookings, Room Keys Assigned, Check-out Trigger"},
                {"id": "eh0_4", "source": "proc_0", "target": "ent_reception", "label": "Occupancy Chart, Expected Arrivals & VIP Notes"},
                {"id": "eh0_5", "source": "ent_housekeeping", "target": "proc_0", "label": "Room Cleaned Status, Minibar Consumption, Service Orders"},
                {"id": "eh0_6", "source": "proc_0", "target": "ent_housekeeping", "label": "Cleaning Priority Queue & Maintenance Requests"},
                {"id": "eh0_7", "source": "proc_0", "target": "ent_accountant", "label": "Night Audit Ledger, Daily Revenue & Tax Reports"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_g", "type": "entity", "label": "Guest", "x": 80, "y": 240, "width": 150, "height": 80},
                {"id": "ent_staff", "type": "entity", "label": "Staff / Reception", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Room Availability & Rate Search", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Advance Reservation Processing", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Guest Check-In & Room Allocation", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Service Billing & Checkout Folio", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_rooms", "type": "datastore", "number": "D1", "label": "Room Inventory & Rates", "x": 720, "y": 130, "width": 210, "height": 60},
                {"id": "ds_bookings", "type": "datastore", "number": "D2", "label": "Guest Reservations Store", "x": 720, "y": 310, "width": 210, "height": 60},
                {"id": "ds_folios", "type": "datastore", "number": "D3", "label": "Billing Folios & Payments", "x": 720, "y": 490, "width": 210, "height": 60}
            ],
            "edges": [
                {"id": "eht1_1", "source": "ent_g", "target": "proc_1_0", "label": "Check-In / Out Dates & Guests"},
                {"id": "eht1_2", "source": "ds_rooms", "target": "proc_1_0", "label": "Vacant Room Types & Pricing"},
                {"id": "eht1_3", "source": "proc_1_0", "target": "ent_g", "label": "Available Rooms & Tariffs"},
                {"id": "eht1_4", "source": "ent_g", "target": "proc_2_0", "label": "Guest Contact & Deposit Info"},
                {"id": "eht1_5", "source": "proc_2_0", "target": "ds_bookings", "label": "Save Reservation Record"},
                {"id": "eht1_6", "source": "ent_staff", "target": "proc_3_0", "label": "Passport Scan & Assign Key"},
                {"id": "eht1_7", "source": "ds_bookings", "target": "proc_3_0", "label": "Fetch Existing Reservation"},
                {"id": "eht1_8", "source": "proc_3_0", "target": "ds_rooms", "label": "Mark Room Status = Occupied"},
                {"id": "eht1_9", "source": "proc_3_0", "target": "ds_folios", "label": "Open Active Guest Folio"},
                {"id": "eht1_10", "source": "ent_staff", "target": "proc_4_0", "label": "Add Dining & Laundry Charges"},
                {"id": "eht1_11", "source": "ds_folios", "target": "proc_4_0", "label": "Consolidated Charges Sum"},
                {"id": "eht1_12", "source": "proc_4_0", "target": "ent_g", "label": "Tax Invoice & Settlement Receipt"},
                {"id": "eht1_13", "source": "proc_4_0", "target": "ds_rooms", "label": "Mark Room = Needs Cleaning"}
            ]
        }
    },
    {
        "slug": "food-delivery-system",
        "title": "Online Food Ordering & Delivery System",
        "category": "On-Demand & Logistics",
        "summary": "Real-time food ordering DFD linking hungry customers, partner restaurants, delivery fleet couriers, and payment processing.",
        "description": "App architecture DFD modeling menu dispatch, cooking queue, GPS delivery assignment, and tip/review collection.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Food Ordering & Delivery Platform", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_cust", "type": "entity", "label": "Customer", "x": 120, "y": 280, "width": 160, "height": 80},
                {"id": "ent_rest", "type": "entity", "label": "Restaurant Partner", "x": 520, "y": 70, "width": 180, "height": 80},
                {"id": "ent_driver", "type": "entity", "label": "Delivery Partner / Driver", "x": 920, "y": 280, "width": 190, "height": 80},
                {"id": "ent_pay", "type": "entity", "label": "Online Payment Gateway", "x": 520, "y": 490, "width": 190, "height": 80}
            ],
            "edges": [
                {"id": "ef0_1", "source": "ent_cust", "target": "proc_0", "label": "Delivery Location, Food Cart, Instructions, Payment"},
                {"id": "ef0_2", "source": "proc_0", "target": "ent_cust", "label": "Menu, Order Receipt, Live Driver GPS, Delivery ETA"},
                {"id": "ef0_3", "source": "proc_0", "target": "ent_rest", "label": "Kitchen Order Ticket (KOT) & Customer Note"},
                {"id": "ef0_4", "source": "ent_rest", "target": "proc_0", "label": "Menu Items, Order Accepted, Food Ready Ping"},
                {"id": "ef0_5", "source": "proc_0", "target": "ent_driver", "label": "Pickup Coordinates, Drop Address, Delivery Fee"},
                {"id": "ef0_6", "source": "ent_driver", "target": "proc_0", "label": "Accept Job, Arrived at Eatery, Order Picked, Order Delivered"},
                {"id": "ef0_7", "source": "proc_0", "target": "ent_pay", "label": "Customer Charge Amount"},
                {"id": "ef0_8", "source": "ent_pay", "target": "proc_0", "label": "Payment Authorization Status"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_c", "type": "entity", "label": "Customer", "x": 80, "y": 240, "width": 150, "height": 80},
                {"id": "ent_d", "type": "entity", "label": "Delivery Driver", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Restaurant Menu Discovery", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Order Placement & Payment", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Kitchen Order Routing", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Delivery Dispatch & GPS Tracking", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_menus", "type": "datastore", "number": "D1", "label": "Restaurant Menus Store", "x": 720, "y": 130, "width": 210, "height": 60},
                {"id": "ds_orders", "type": "datastore", "number": "D2", "label": "Active Food Orders Store", "x": 720, "y": 310, "width": 210, "height": 60},
                {"id": "ds_tracking", "type": "datastore", "number": "D3", "label": "Driver Telemetry & Tracking", "x": 720, "y": 490, "width": 210, "height": 60}
            ],
            "edges": [
                {"id": "ef1_1", "source": "ent_c", "target": "proc_1_0", "label": "GPS Coordinates & Cuisines"},
                {"id": "ef1_2", "source": "ds_menus", "target": "proc_1_0", "label": "Nearby Restaurants & Items"},
                {"id": "ef1_3", "source": "proc_1_0", "target": "ent_c", "label": "Dish Listings & Pricing"},
                {"id": "ef1_4", "source": "ent_c", "target": "proc_2_0", "label": "Place Order & Pay"},
                {"id": "ef1_5", "source": "proc_2_0", "target": "ds_orders", "label": "Create Order Status = Placed"},
                {"id": "ef1_6", "source": "ds_orders", "target": "proc_3_0", "label": "New Order Alert for Eatery"},
                {"id": "ef1_7", "source": "proc_3_0", "target": "ds_orders", "label": "Update Status = Cooking / Ready"},
                {"id": "ef1_8", "source": "proc_3_0", "target": "proc_4_0", "label": "Trigger Nearby Courier Broadcast"},
                {"id": "ef1_9", "source": "proc_4_0", "target": "ent_d", "label": "Dispatch Offer to Driver App"},
                {"id": "ef1_10", "source": "ent_d", "target": "proc_4_0", "label": "Accept Offer + Live Coordinates"},
                {"id": "ef1_11", "source": "proc_4_0", "target": "ds_tracking", "label": "Stream GPS Coordinates"},
                {"id": "ef1_12", "source": "ds_tracking", "target": "ent_c", "label": "Real-time Map ETA Stream"}
            ]
        }
    },
    {
        "slug": "digital-library-management",
        "title": "Digital Library Management System",
        "category": "Education & Academic",
        "summary": "Classic software engineering textbook DFD covering book catalog search, member borrowing, return processing, overdue fine calculation, and book reservation.",
        "description": "Standard university DFD model mapping students, faculty patrons, and chief librarian.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Digital Library System", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_member", "type": "entity", "label": "Library Member / Student", "x": 120, "y": 280, "width": 170, "height": 80},
                {"id": "ent_librarian", "type": "entity", "label": "Librarian / Staff", "x": 520, "y": 70, "width": 180, "height": 80},
                {"id": "ent_vendor", "type": "entity", "label": "Book Publisher / Vendor", "x": 920, "y": 280, "width": 180, "height": 80}
            ],
            "edges": [
                {"id": "el0_1", "source": "ent_member", "target": "proc_0", "label": "Book Search, Borrow Request, Book Return, Fine Payment"},
                {"id": "el0_2", "source": "proc_0", "target": "ent_member", "label": "Catalog Results, Due Date Slip, Overdue Alert, Fine Receipt"},
                {"id": "el0_3", "source": "ent_librarian", "target": "proc_0", "label": "Add New Book, Update Shelf, Issue Book, Waive Fine"},
                {"id": "el0_4", "source": "proc_0", "target": "ent_librarian", "label": "Overdue Defaulters List, Inventory Audit Report"},
                {"id": "el0_5", "source": "proc_0", "target": "ent_vendor", "label": "Book Purchase Requisition Order"},
                {"id": "el0_6", "source": "ent_vendor", "target": "proc_0", "label": "Book Delivery Manifest & Invoice"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_m", "type": "entity", "label": "Member", "x": 80, "y": 240, "width": 150, "height": 80},
                {"id": "ent_lib", "type": "entity", "label": "Librarian", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Catalog Search & Availability", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Issue & Loan Processing", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Return & Fine Calculation", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Catalog & Inventory Maintenance", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_books", "type": "datastore", "number": "D1", "label": "Books Master Catalog", "x": 720, "y": 130, "width": 210, "height": 60},
                {"id": "ds_members", "type": "datastore", "number": "D2", "label": "Patrons & Borrow Limits", "x": 720, "y": 310, "width": 210, "height": 60},
                {"id": "ds_loans", "type": "datastore", "number": "D3", "label": "Active Book Loans & Fines", "x": 720, "y": 490, "width": 210, "height": 60}
            ],
            "edges": [
                {"id": "el1_1", "source": "ent_m", "target": "proc_1_0", "label": "Title / Author / ISBN Query"},
                {"id": "el1_2", "source": "ds_books", "target": "proc_1_0", "label": "Available Shelf Location"},
                {"id": "el1_3", "source": "proc_1_0", "target": "ent_m", "label": "Book Details & Rack Number"},
                {"id": "el1_4", "source": "ent_m", "target": "proc_2_0", "label": "Scan Member Card + Book Barcode"},
                {"id": "el1_5", "source": "ds_members", "target": "proc_2_0", "label": "Check Active Borrow Count"},
                {"id": "el1_6", "source": "proc_2_0", "target": "ds_books", "label": "Decrement Available Copies"},
                {"id": "el1_7", "source": "proc_2_0", "target": "ds_loans", "label": "Create Loan (Issue Date + Due Date)"},
                {"id": "el1_8", "source": "proc_2_0", "target": "ent_m", "label": "Printed Stamped Due Date"},
                {"id": "el1_9", "source": "ent_m", "target": "proc_3_0", "label": "Return Book Barcode"},
                {"id": "el1_10", "source": "ds_loans", "target": "proc_3_0", "label": "Fetch Original Due Date"},
                {"id": "el1_11", "source": "proc_3_0", "target": "ds_books", "label": "Increment Available Stock"},
                {"id": "el1_12", "source": "proc_3_0", "target": "ds_loans", "label": "Record Return Timestamp & Fine Due"},
                {"id": "el1_13", "source": "ent_lib", "target": "proc_4_0", "label": "Add New Book Acquisition"},
                {"id": "el1_14", "source": "proc_4_0", "target": "ds_books", "label": "Insert Book Catalog Record"}
            ]
        }
    },
    {
        "slug": "ride-hailing-system",
        "title": "Ride-Hailing & Taxi Dispatch System",
        "category": "Travel & Transportation",
        "summary": "Uber/Lyft style real-time geospatial taxi dispatch system DFD mapping riders, drivers, surge pricing, routing, and mobile payments.",
        "description": "Geospatial on-demand transport DFD linking smartphone clients, telemetry streaming, geospatial matching, and automated fare settlement.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Ride Hailing Dispatch System", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_rider", "type": "entity", "label": "Passenger / Rider", "x": 120, "y": 280, "width": 160, "height": 80},
                {"id": "ent_driver", "type": "entity", "label": "Cab Driver", "x": 520, "y": 70, "width": 180, "height": 80},
                {"id": "ent_maps", "type": "entity", "label": "Mapping & Routing API", "x": 920, "y": 280, "width": 190, "height": 80},
                {"id": "ent_payment", "type": "entity", "label": "Payment Processor", "x": 520, "y": 490, "width": 180, "height": 80}
            ],
            "edges": [
                {"id": "er0_1", "source": "ent_rider", "target": "proc_0", "label": "Pickup, Destination, Ride Type (Sedan/SUV), Payment Token"},
                {"id": "er0_2", "source": "proc_0", "target": "ent_rider", "label": "Upfront Fare, Assigned Cab Details, Live Driver Location, E-Receipt"},
                {"id": "er0_3", "source": "ent_driver", "target": "proc_0", "label": "Driver Status (Online/Busy), GPS Coordinates, Accept/Reject Ping"},
                {"id": "er0_4", "source": "proc_0", "target": "ent_driver", "label": "Ride Dispatch Request, Rider Pickup Pin, Payout Statements"},
                {"id": "er0_5", "source": "proc_0", "target": "ent_maps", "label": "Origin/Destination Lat-Long Coordinates"},
                {"id": "er0_6", "source": "ent_maps", "target": "proc_0", "label": "Estimated Travel Duration, Turn-by-Turn Route, Distance Matrix"},
                {"id": "er0_7", "source": "proc_0", "target": "ent_payment", "label": "Automatic Fare Debit Payload"},
                {"id": "er0_8", "source": "ent_payment", "target": "proc_0", "label": "Transaction Status & Receipt ID"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_r", "type": "entity", "label": "Rider", "x": 80, "y": 240, "width": 150, "height": 80},
                {"id": "ent_d", "type": "entity", "label": "Driver", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Fare Estimate & Surge Calculation", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Geospatial Matching & Driver Dispatch", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Live Trip Telemetry & Metering", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Fare Settlement & Driver Payout", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_drivers", "type": "datastore", "number": "D1", "label": "Active Drivers & Geospatial Index", "x": 720, "y": 130, "width": 220, "height": 60},
                {"id": "ds_trips", "type": "datastore", "number": "D2", "label": "Trips & Fares Store", "x": 720, "y": 310, "width": 220, "height": 60},
                {"id": "ds_wallets", "type": "datastore", "number": "D3", "label": "User Wallets & Driver Payouts", "x": 720, "y": 490, "width": 220, "height": 60}
            ],
            "edges": [
                {"id": "er1_1", "source": "ent_r", "target": "proc_1_0", "label": "Request Ride Quote"},
                {"id": "er1_2", "source": "ds_drivers", "target": "proc_1_0", "label": "Driver Density in Surge Zone"},
                {"id": "er1_3", "source": "proc_1_0", "target": "ent_r", "label": "Estimated Price Quote"},
                {"id": "er1_4", "source": "ent_r", "target": "proc_2_0", "label": "Confirm Booking Request"},
                {"id": "er1_5", "source": "ds_drivers", "target": "proc_2_0", "label": "Query Nearest Idle Drivers"},
                {"id": "er1_6", "source": "proc_2_0", "target": "ent_d", "label": "Dispatch Trip Notification"},
                {"id": "er1_7", "source": "ent_d", "target": "proc_2_0", "label": "Driver Accept Ride"},
                {"id": "er1_8", "source": "proc_2_0", "target": "ds_trips", "label": "Init Trip Record Status = Dispatched"},
                {"id": "er1_9", "source": "ent_d", "target": "proc_3_0", "label": "Start Trip OTP + Continuous GPS Stream"},
                {"id": "er1_10", "source": "proc_3_0", "target": "ds_trips", "label": "Record Actual Odometer Distance & Time"},
                {"id": "er1_11", "source": "proc_3_0", "target": "proc_4_0", "label": "Trip Complete Trigger"},
                {"id": "er1_12", "source": "proc_4_0", "target": "ds_wallets", "label": "Debit Rider Wallet & Credit Driver Account"},
                {"id": "er1_13", "source": "proc_4_0", "target": "ent_r", "label": "Send Detailed Fare Breakdown"}
            ]
        }
    },
    {
        "slug": "social-media-platform",
        "title": "Social Media Platform (Posts, Friends, Feed)",
        "category": "Social & Media",
        "summary": "Full social network data flow modeling user profiles, friendship connections, multimedia post publishing, algorithmic feed ranking, and notifications.",
        "description": "High-throughput content sharing DFD connecting creators, followers, content moderation safety algorithms, and advertising engines.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Social Media Platform", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_user", "type": "entity", "label": "Social Media User", "x": 120, "y": 280, "width": 160, "height": 80},
                {"id": "ent_advertiser", "type": "entity", "label": "Brand Advertiser", "x": 520, "y": 70, "width": 180, "height": 80},
                {"id": "ent_moderator", "type": "entity", "label": "Trust & Safety Moderator", "x": 920, "y": 280, "width": 190, "height": 80},
                {"id": "ent_cdn", "type": "entity", "label": "Media CDN & Storage", "x": 520, "y": 490, "width": 180, "height": 80}
            ],
            "edges": [
                {"id": "esm0_1", "source": "ent_user", "target": "proc_0", "label": "Post Content, Photos/Videos, Likes, Comments, Friend Invites"},
                {"id": "esm0_2", "source": "proc_0", "target": "ent_user", "label": "Ranked News Feed, Notifications, Direct Messages, Trending Topics"},
                {"id": "esm0_3", "source": "ent_advertiser", "target": "proc_0", "label": "Sponsored Ads, Target Demographics, Budget Cap"},
                {"id": "esm0_4", "source": "proc_0", "target": "ent_advertiser", "label": "Ad Impressions, Click-Through Rates (CTR), Conversion Analytics"},
                {"id": "esm0_5", "source": "proc_0", "target": "ent_moderator", "label": "Flagged Posts, Spam Reports, Policy Violation Queue"},
                {"id": "esm0_6", "source": "ent_moderator", "target": "proc_0", "label": "Content Takedown Decisions & User Strike Penalties"},
                {"id": "esm0_7", "source": "proc_0", "target": "ent_cdn", "label": "Raw Video & Image Upload Chunks"},
                {"id": "esm0_8", "source": "ent_cdn", "target": "proc_0", "label": "Optimized Media URLs & HLS Video Playlists"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_u", "type": "entity", "label": "User", "x": 80, "y": 240, "width": 150, "height": 80},
                {"id": "ent_mod", "type": "entity", "label": "Moderator", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Profile & Social Graph Management", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Post Ingestion & Media Encoding", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Personalized Feed Generation", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Social Interactions & Notifications", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_users", "type": "datastore", "number": "D1", "label": "User Accounts & Friends Graph", "x": 720, "y": 130, "width": 220, "height": 60},
                {"id": "ds_posts", "type": "datastore", "number": "D2", "label": "Posts, Comments & Media Metadata", "x": 720, "y": 310, "width": 220, "height": 60},
                {"id": "ds_feedcache", "type": "datastore", "number": "D3", "label": "User Feed Caches & Activity Log", "x": 720, "y": 490, "width": 220, "height": 60}
            ],
            "edges": [
                {"id": "esm1_1", "source": "ent_u", "target": "proc_1_0", "label": "Follow / Friend Request"},
                {"id": "esm1_2", "source": "proc_1_0", "target": "ds_users", "label": "Update Friendship Connection"},
                {"id": "esm1_3", "source": "ent_u", "target": "proc_2_0", "label": "Upload Post & Media File"},
                {"id": "esm1_4", "source": "proc_2_0", "target": "ds_posts", "label": "Store Post Record"},
                {"id": "esm1_5", "source": "proc_2_0", "target": "proc_3_0", "label": "Fan-Out Post to Followers"},
                {"id": "esm1_6", "source": "ds_users", "target": "proc_3_0", "label": "Fetch Follower List"},
                {"id": "esm1_7", "source": "proc_3_0", "target": "ds_feedcache", "label": "Precompute Timeline Feeds"},
                {"id": "esm1_8", "source": "ds_feedcache", "target": "proc_3_0", "label": "Read Ranked Posts"},
                {"id": "esm1_9", "source": "proc_3_0", "target": "ent_u", "label": "Stream Home Feed"},
                {"id": "esm1_10", "source": "ent_u", "target": "proc_4_0", "label": "Like Post / Submit Comment"},
                {"id": "esm1_11", "source": "proc_4_0", "target": "ds_posts", "label": "Increment Reaction Counter"},
                {"id": "esm1_12", "source": "proc_4_0", "target": "ent_u", "label": "Push Instant Notification"}
            ]
        }
    },
    {
        "slug": "inventory-warehouse-logistics",
        "title": "Warehouse Inventory & Supply Chain Logistics",
        "category": "Logistics & Manufacturing",
        "summary": "Enterprise supply chain DFD modeling purchase orders, stock receipt, warehouse binning, pick-and-pack, reorder thresholds, and vendor dispatch.",
        "description": "B2B inventory management DFD connecting warehouse managers, suppliers, floor pickers, and ERP accounting systems.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Warehouse Inventory System", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_manager", "type": "entity", "label": "Warehouse Inventory Manager", "x": 120, "y": 280, "width": 190, "height": 80},
                {"id": "ent_supplier", "type": "entity", "label": "Raw Materials Supplier", "x": 520, "y": 70, "width": 190, "height": 80},
                {"id": "ent_picker", "type": "entity", "label": "Warehouse Floor Staff", "x": 920, "y": 280, "width": 180, "height": 80},
                {"id": "ent_erp", "type": "entity", "label": "Enterprise Financial ERP", "x": 520, "y": 490, "width": 190, "height": 80}
            ],
            "edges": [
                {"id": "ei0_1", "source": "ent_manager", "target": "proc_0", "label": "Reorder Level Triggers, Stock Adjustments, SKU Rules"},
                {"id": "ei0_2", "source": "proc_0", "target": "ent_manager", "label": "Stock Valuations, Out-of-Stock Alerts, Inventory Turnover"},
                {"id": "ei0_3", "source": "proc_0", "target": "ent_supplier", "label": "Automated Purchase Order (PO) Requisitions"},
                {"id": "ei0_4", "source": "ent_supplier", "target": "proc_0", "label": "Goods Receipt Note (GRN) & Inbound Consignment"},
                {"id": "ei0_5", "source": "proc_0", "target": "ent_picker", "label": "Wave Pick Lists & Aisle/Shelf Routing Instructions"},
                {"id": "ei0_6", "source": "ent_picker", "target": "proc_0", "label": "Barcode Scans, Bin Confirmation, Damage Logs"},
                {"id": "ei0_7", "source": "proc_0", "target": "ent_erp", "label": "Cost of Goods Sold (COGS) & Asset Depreciation"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_mfg", "type": "entity", "label": "Inventory Mgr", "x": 80, "y": 240, "width": 150, "height": 80},
                {"id": "ent_supp", "type": "entity", "label": "Supplier", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Inbound Receiving & Quality Inspection", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Stock Tracking & Bin Management", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Outbound Pick, Pack & Shipping", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Automated Reorder & PO Generation", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_items", "type": "datastore", "number": "D1", "label": "Item Master & Stock Levels", "x": 720, "y": 130, "width": 220, "height": 60},
                {"id": "ds_locations", "type": "datastore", "number": "D2", "label": "Warehouse Bin & Rack Locations", "x": 720, "y": 310, "width": 220, "height": 60},
                {"id": "ds_pos", "type": "datastore", "number": "D3", "label": "Purchase Orders & Vendor Contracts", "x": 720, "y": 490, "width": 220, "height": 60}
            ],
            "edges": [
                {"id": "ei1_1", "source": "ent_supp", "target": "proc_1_0", "label": "Inbound Delivery & Packing Slip"},
                {"id": "ei1_2", "source": "proc_1_0", "target": "ds_items", "label": "Increment Available Stock Count"},
                {"id": "ei1_3", "source": "proc_1_0", "target": "proc_2_0", "label": "Putaway Notification"},
                {"id": "ei1_4", "source": "proc_2_0", "target": "ds_locations", "label": "Map SKU to Specific Aisle/Bin"},
                {"id": "ei1_5", "source": "ds_locations", "target": "proc_3_0", "label": "Fetch Nearest Picking Path"},
                {"id": "ei1_6", "source": "proc_3_0", "target": "ds_items", "label": "Decrement Shipped Quantity"},
                {"id": "ei1_7", "source": "ds_items", "target": "proc_4_0", "label": "Trigger Threshold: Stock < MinReorder"},
                {"id": "ei1_8", "source": "ds_pos", "target": "proc_4_0", "label": "Preferred Vendor Pricing"},
                {"id": "ei1_9", "source": "proc_4_0", "target": "ent_supp", "label": "Issue Purchase Order (PO)"},
                {"id": "ei1_10", "source": "proc_4_0", "target": "ds_pos", "label": "Save Pending Requisition Record"}
            ]
        }
    },
    {
        "slug": "payroll-hr-management",
        "title": "Payroll, Attendance & HR Management System",
        "category": "Human Resources & Payroll",
        "summary": "Covers biometric employee attendance, leave management, tax deduction, provident fund (PF/401k), net salary disbursement, and payslip generation.",
        "description": "Standard corporate enterprise DFD connecting corporate employees, HR managers, tax authorities, and corporate commercial banks.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Payroll & HR Management System", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_emp", "type": "entity", "label": "Corporate Employee", "x": 120, "y": 280, "width": 170, "height": 80},
                {"id": "ent_hr", "type": "entity", "label": "HR Director / Manager", "x": 520, "y": 70, "width": 180, "height": 80},
                {"id": "ent_bank", "type": "entity", "label": "Corporate Salary Bank", "x": 920, "y": 280, "width": 180, "height": 80},
                {"id": "ent_tax", "type": "entity", "label": "Internal Revenue / Tax Dept", "x": 520, "y": 490, "width": 190, "height": 80}
            ],
            "edges": [
                {"id": "ep0_1", "source": "ent_emp", "target": "proc_0", "label": "Biometric Clock-In, Leave Requests, Tax Declarations"},
                {"id": "ep0_2", "source": "proc_0", "target": "ent_emp", "label": "Monthly Payslip PDF, Leave Balance, Annual Tax Form"},
                {"id": "ep0_3", "source": "ent_hr", "target": "proc_0", "label": "Salary Increments, Bonus Allocations, New Hires / Exits"},
                {"id": "ep0_4", "source": "proc_0", "target": "ent_hr", "label": "Monthly Headcount, Absenteeism, Total Salary Outflow"},
                {"id": "ep0_5", "source": "proc_0", "target": "ent_bank", "label": "Automated Clearing House (ACH) Direct Deposit File"},
                {"id": "ep0_6", "source": "ent_bank", "target": "proc_0", "label": "Disbursement Ack & Rejected Account List"},
                {"id": "ep0_7", "source": "proc_0", "target": "ent_tax", "label": "Statutory TDS Withholding & Social Security Returns"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_e", "type": "entity", "label": "Employee", "x": 80, "y": 240, "width": 150, "height": 80},
                {"id": "ent_b", "type": "entity", "label": "Corporate Bank", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Attendance & Leave Tracking", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Salary Computation & Deductions", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Bank Transfer & ACH File Generation", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Payslip & Statutory Compliance", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_emp", "type": "datastore", "number": "D1", "label": "Employee Profile & Pay Structure", "x": 720, "y": 130, "width": 220, "height": 60},
                {"id": "ds_attendance", "type": "datastore", "number": "D2", "label": "Monthly Timesheets & Leaves", "x": 720, "y": 310, "width": 220, "height": 60},
                {"id": "ds_payroll", "type": "datastore", "number": "D3", "label": "Payroll Master & Tax Ledger", "x": 720, "y": 490, "width": 220, "height": 60}
            ],
            "edges": [
                {"id": "ep1_1", "source": "ent_e", "target": "proc_1_0", "label": "Daily Swipe Timestamp & Leave Form"},
                {"id": "ep1_2", "source": "proc_1_0", "target": "ds_attendance", "label": "Calculate Payable Days"},
                {"id": "ep1_3", "source": "ds_attendance", "target": "proc_2_0", "label": "Approved Working Days Count"},
                {"id": "ep1_4", "source": "ds_emp", "target": "proc_2_0", "label": "Basic Pay, HRA, Medical Allowances"},
                {"id": "ep1_5", "source": "proc_2_0", "target": "ds_payroll", "label": "Write Computed Gross & Net Pay"},
                {"id": "ep1_6", "source": "ds_payroll", "target": "proc_3_0", "label": "Net Salary Batch List"},
                {"id": "ep1_7", "source": "proc_3_0", "target": "ent_b", "label": "Bank Direct Deposit File"},
                {"id": "ep1_8", "source": "ds_payroll", "target": "proc_4_0", "label": "Itemized Earnings & Deductions"},
                {"id": "ep1_9", "source": "proc_4_0", "target": "ent_e", "label": "Deliver Encrypted Payslip PDF"}
            ]
        }
    },
    {
        "slug": "online-examination-proctoring",
        "title": "Online Examination & Automated Proctoring",
        "category": "Education & Assessment",
        "summary": "Online assessment platform modeling question bank randomization, candidate test delivery, automated webcam/audio AI proctoring, and instant grade evaluation.",
        "description": "Standard university testing DFD connecting students, course instructors, remote human proctors, and certificate issuers.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Online Examination System", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_candidate", "type": "entity", "label": "Exam Candidate / Student", "x": 120, "y": 280, "width": 180, "height": 80},
                {"id": "ent_faculty", "type": "entity", "label": "Examiner / Faculty", "x": 520, "y": 70, "width": 180, "height": 80},
                {"id": "ent_proctor", "type": "entity", "label": "AI / Human Remote Proctor", "x": 920, "y": 280, "width": 200, "height": 80},
                {"id": "ent_cert", "type": "entity", "label": "Certification Authority", "x": 520, "y": 490, "width": 190, "height": 80}
            ],
            "edges": [
                {"id": "eex0_1", "source": "ent_candidate", "target": "proc_0", "label": "Biometric Auth, Test Answers, Webcam/Audio Stream"},
                {"id": "eex0_2", "source": "proc_0", "target": "ent_candidate", "label": "Test Questions, Timer, Score Card & Result"},
                {"id": "eex0_3", "source": "ent_faculty", "target": "proc_0", "label": "Question Banks, Rubrics, Passing Thresholds"},
                {"id": "eex0_4", "source": "proc_0", "target": "ent_faculty", "label": "Class Score Distribution, Anomaly Reports"},
                {"id": "eex0_5", "source": "proc_0", "target": "ent_proctor", "label": "Live Video Feed & Window Focus Events"},
                {"id": "eex0_6", "source": "ent_proctor", "target": "proc_0", "label": "Malpractice Flag & Exam Termination"},
                {"id": "eex0_7", "source": "proc_0", "target": "ent_cert", "label": "Verified Pass List & Score Metadata"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_cand", "type": "entity", "label": "Candidate", "x": 80, "y": 240, "width": 150, "height": 80},
                {"id": "ent_eval", "type": "entity", "label": "Examiner", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Authentication & Environment Check", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Question Paper Rendering & Timer", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Automated Proctoring & AI Telemetry", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Response Evaluation & Result Publish", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_questions", "type": "datastore", "number": "D1", "label": "Question Bank & Answer Keys", "x": 720, "y": 130, "width": 220, "height": 60},
                {"id": "ds_responses", "type": "datastore", "number": "D2", "label": "Candidate Answer Submissions", "x": 720, "y": 310, "width": 220, "height": 60},
                {"id": "ds_proctorlogs", "type": "datastore", "number": "D3", "label": "AI Proctoring Incident Logs", "x": 720, "y": 490, "width": 220, "height": 60}
            ],
            "edges": [
                {"id": "eex1_1", "source": "ent_cand", "target": "proc_1_0", "label": "Student ID & Webcam Snapshot"},
                {"id": "eex1_2", "source": "proc_1_0", "target": "proc_2_0", "label": "Verified Exam Session"},
                {"id": "eex1_3", "source": "ds_questions", "target": "proc_2_0", "label": "Randomized Question Set"},
                {"id": "eex1_4", "source": "proc_2_0", "target": "ent_cand", "label": "Stream Test Questions"},
                {"id": "eex1_5", "source": "ent_cand", "target": "proc_3_0", "label": "Webcam Feed & Eye-Tracking Data"},
                {"id": "eex1_6", "source": "proc_3_0", "target": "ds_proctorlogs", "label": "Log Suspicious Movement Warnings"},
                {"id": "eex1_7", "source": "ent_cand", "target": "proc_4_0", "label": "Submit Final Answers"},
                {"id": "eex1_8", "source": "proc_4_0", "target": "ds_responses", "label": "Save Candidate Answers"},
                {"id": "eex1_9", "source": "ds_questions", "target": "proc_4_0", "label": "Fetch Correct Answer Keys"},
                {"id": "eex1_10", "source": "proc_4_0", "target": "ent_cand", "label": "Display Final Exam Score Card"}
            ]
        }
    },
    {
        "slug": "railway-ticket-reservation",
        "title": "Railway Ticket Booking & Train Tracking",
        "category": "Travel & Transportation",
        "summary": "IRCTC/Amtrak style railway reservation DFD modeling passenger train schedules, berth quota allocation (Sleeper, AC), waitlist confirmation, and e-ticket issuance.",
        "description": "High-volume public transit DFD connecting railway passengers, station ticket clerks, and train ticket examiners (TTE).",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Railway Reservation System", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_passenger", "type": "entity", "label": "Train Passenger", "x": 120, "y": 280, "width": 170, "height": 80},
                {"id": "ent_clerk", "type": "entity", "label": "Station Ticket Clerk", "x": 520, "y": 70, "width": 180, "height": 80},
                {"id": "ent_tte", "type": "entity", "label": "Train Ticket Examiner (TTE)", "x": 920, "y": 280, "width": 200, "height": 80},
                {"id": "ent_bank", "type": "entity", "label": "Banking Gateway", "x": 520, "y": 490, "width": 180, "height": 80}
            ],
            "edges": [
                {"id": "erw0_1", "source": "ent_passenger", "target": "proc_0", "label": "Source, Destination, Train No, Class Quota, Passenger Age"},
                {"id": "erw0_2", "source": "proc_0", "target": "ent_passenger", "label": "10-Digit PNR, Coach/Berth Number, Cancellation Refund"},
                {"id": "erw0_3", "source": "ent_clerk", "target": "proc_0", "label": "Counter Bookings, Emergency Quota Releases"},
                {"id": "erw0_4", "source": "proc_0", "target": "ent_clerk", "label": "Station Daily Cash Collections & PNR Inquiry"},
                {"id": "erw0_5", "source": "proc_0", "target": "ent_tte", "label": "Electronic Reservation Chart & Empty Berth List"},
                {"id": "erw0_6", "source": "ent_tte", "target": "proc_0", "label": "Onboard Attendance & No-Show Vacancy Update"},
                {"id": "erw0_7", "source": "proc_0", "target": "ent_bank", "label": "Ticket Fare Charge Payload"},
                {"id": "erw0_8", "source": "ent_bank", "target": "proc_0", "label": "Payment Authorization Code"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_p", "type": "entity", "label": "Passenger", "x": 80, "y": 240, "width": 150, "height": 80},
                {"id": "ent_tte_app", "type": "entity", "label": "TTE Device", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Train Schedule & Seat Availability", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Berth Allocation & PNR Generation", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Payment Checkout & Ticket Issue", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Final Reservation Charting", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_trains", "type": "datastore", "number": "D1", "label": "Train Timetables & Quotas", "x": 720, "y": 130, "width": 220, "height": 60},
                {"id": "ds_pnrs", "type": "datastore", "number": "D2", "label": "Passenger PNR Master Store", "x": 720, "y": 310, "width": 220, "height": 60},
                {"id": "ds_charts", "type": "datastore", "number": "D3", "label": "Train Coach Reservation Charts", "x": 720, "y": 490, "width": 220, "height": 60}
            ],
            "edges": [
                {"id": "erw1_1", "source": "ent_p", "target": "proc_1_0", "label": "Station Pair & Travel Date"},
                {"id": "erw1_2", "source": "ds_trains", "target": "proc_1_0", "label": "Available Berths & Waitlist Status"},
                {"id": "erw1_3", "source": "proc_1_0", "target": "ent_p", "label": "Train Options & Fare Quote"},
                {"id": "erw1_4", "source": "ent_p", "target": "proc_2_0", "label": "Passenger Details & Berth Preference"},
                {"id": "erw1_5", "source": "proc_2_0", "target": "ds_pnrs", "label": "Generate PNR (Status = Booked/WL)"},
                {"id": "erw1_6", "source": "proc_2_0", "target": "proc_3_0", "label": "Forward PNR for Fare Payment"},
                {"id": "erw1_7", "source": "proc_3_0", "target": "ent_p", "label": "Send Confirmed E-Ticket SMS"},
                {"id": "erw1_8", "source": "ds_pnrs", "target": "proc_4_0", "label": "Consolidate Confirmed Passengers"},
                {"id": "erw1_9", "source": "proc_4_0", "target": "ds_charts", "label": "Freeze Coach Berth Manifest"},
                {"id": "erw1_10", "source": "ds_charts", "target": "ent_tte_app", "label": "Transmit Chart to TTE Tablet"}
            ]
        }
    },
    {
        "slug": "car-rental-fleet-management",
        "title": "Vehicle Rental & Fleet Management System",
        "category": "Travel & Transportation",
        "summary": "Full rental operations DFD modeling vehicle catalog browsing, driver license verification, rental contract agreement, telemetry GPS return tracking, and damage deposit refund.",
        "description": "Automotive fleet DFD connecting car renters, rental depot managers, road assistance mechanics, and insurance adjusters.",
        "level0": {
            "nodes": [
                {"id": "proc_0", "type": "process", "number": "0", "label": "Vehicle Rental Management System", "x": 520, "y": 280, "width": 240, "height": 110},
                {"id": "ent_customer", "type": "entity", "label": "Car Renter / Customer", "x": 120, "y": 280, "width": 170, "height": 80},
                {"id": "ent_depot", "type": "entity", "label": "Depot Fleet Manager", "x": 520, "y": 70, "width": 180, "height": 80},
                {"id": "ent_telematics", "type": "entity", "label": "Vehicle IoT Telematics Device", "x": 920, "y": 280, "width": 210, "height": 80},
                {"id": "ent_payment", "type": "entity", "label": "Payment / Security Deposit Gateway", "x": 520, "y": 490, "width": 220, "height": 80}
            ],
            "edges": [
                {"id": "ecr0_1", "source": "ent_customer", "target": "proc_0", "label": "Vehicle Class, Rental Dates, Driving License, Security Deposit"},
                {"id": "ecr0_2", "source": "proc_0", "target": "ent_customer", "label": "Rental Agreement, Digital Key Access, Fuel Policy, Invoice"},
                {"id": "ecr0_3", "source": "ent_depot", "target": "proc_0", "label": "Vehicle Fleet Additions, Scheduled Service Records"},
                {"id": "ecr0_4", "source": "proc_0", "target": "ent_depot", "label": "Fleet Utilization, Overdue Returns, Maintenance Warnings"},
                {"id": "ecr0_5", "source": "ent_telematics", "target": "proc_0", "label": "Odometer Mileage, GPS Location, Fuel Level Telemetry"},
                {"id": "ecr0_6", "source": "proc_0", "target": "ent_telematics", "label": "Remote Door Unlock / Immobilize Command"},
                {"id": "ecr0_7", "source": "proc_0", "target": "ent_payment", "label": "Hold Pre-Authorization Deposit & Final Charge"},
                {"id": "ecr0_8", "source": "ent_payment", "target": "proc_0", "label": "Deposit Release & Transaction Auth"}
            ]
        },
        "level1": {
            "nodes": [
                {"id": "ent_renter", "type": "entity", "label": "Renter", "x": 80, "y": 240, "width": 150, "height": 80},
                {"id": "ent_manager", "type": "entity", "label": "Depot Mgr", "x": 1050, "y": 240, "width": 160, "height": 80},
                {"id": "proc_1_0", "type": "process", "number": "1.0", "label": "Fleet Search & License Validation", "x": 380, "y": 90, "width": 220, "height": 75},
                {"id": "proc_2_0", "type": "process", "number": "2.0", "label": "Reservation & Rental Agreement", "x": 380, "y": 230, "width": 220, "height": 75},
                {"id": "proc_3_0", "type": "process", "number": "3.0", "label": "Vehicle Handover & IoT Unlock", "x": 380, "y": 370, "width": 220, "height": 75},
                {"id": "proc_4_0", "type": "process", "number": "4.0", "label": "Vehicle Return Inspection & Settlement", "x": 380, "y": 510, "width": 220, "height": 75},
                {"id": "ds_fleet", "type": "datastore", "number": "D1", "label": "Vehicle Fleet & Status Store", "x": 720, "y": 130, "width": 220, "height": 60},
                {"id": "ds_contracts", "type": "datastore", "number": "D2", "label": "Rental Contracts & Insurance", "x": 720, "y": 310, "width": 220, "height": 60},
                {"id": "ds_inspections", "type": "datastore", "number": "D3", "label": "Check-In / Out Vehicle Logs", "x": 720, "y": 490, "width": 220, "height": 60}
            ],
            "edges": [
                {"id": "ecr1_1", "source": "ent_renter", "target": "proc_1_0", "label": "Driver License & Preferred Dates"},
                {"id": "ecr1_2", "source": "ds_fleet", "target": "proc_1_0", "label": "Available Vehicles in Depot"},
                {"id": "ecr1_3", "source": "proc_1_0", "target": "ent_renter", "label": "Vehicle Choices & Rates"},
                {"id": "ecr1_4", "source": "ent_renter", "target": "proc_2_0", "label": "Sign Rental Agreement & Pay Deposit"},
                {"id": "ecr1_5", "source": "proc_2_0", "target": "ds_contracts", "label": "Save Executed Rental Contract"},
                {"id": "ecr1_6", "source": "proc_2_0", "target": "ds_fleet", "label": "Mark Car Status = Reserved"},
                {"id": "ecr1_7", "source": "proc_3_0", "target": "ent_renter", "label": "Digital Key Access on Mobile"},
                {"id": "ecr1_8", "source": "ent_renter", "target": "proc_4_0", "label": "Return Vehicle at Drop Depot"},
                {"id": "ecr1_9", "source": "proc_4_0", "target": "ds_inspections", "label": "Record Fuel Level & Damage Check"},
                {"id": "ecr1_10", "source": "proc_4_0", "target": "ds_fleet", "label": "Mark Car Status = Available for Cleaning"},
                {"id": "ecr1_11", "source": "proc_4_0", "target": "ent_renter", "label": "Refund Security Deposit & Final Invoice"}
            ]
        }
    }
]
