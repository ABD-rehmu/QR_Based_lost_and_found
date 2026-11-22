# CampusTag (QR Base IDT26)
### QR-Based "Instant Match" Campus Lost & Found System
**Platform:** Mobile-First Web Application (PWA) with Security Desk & Admin Dashboard  
**Compliant with:** PRD Version 1.0 (India DPDP Act & Privacy Preserving Standards)

---

## 🌟 Key Pillars & Features

### 1. Registered QR Tags & Item Registry (QR-1 to QR-7)
- **Zero-PII Random Tokens:** QR codes contain only cryptographic non-guessable tokens (e.g. `cpt_macbook88a`). No student email, phone number, or roll number is encoded.
- **Zero-Install Public Finder Page (`/t/{token}`):** Anyone with an iPhone or Android camera can scan and load the finder page in under 2 seconds without downloading any app or creating an account.
- **Printable Sticker Sheet (`/print-sheet`):** Generates high-resolution sticker sheets with cut lines, QR codes, and campus return instructions for thermal labels or standard paper.
- **1-Click "Mark as Lost" Toggle:** Owners can toggle lost status, which immediately paints the public scan page with a high-priority "OWNER REPORTED LOST" alert.
- **Compromise Protection:** Owners can deactivate or regenerate QR tokens at any time (QR-6).

### 2. Multi-Signal Instant Match Engine (MT-1 to MT-8)
- Executes in real-time within milliseconds of report submission.
- **Algorithm Signals:**
  1. **Category Filter (35% weight):** Hard and soft compatible taxonomy matching.
  2. **Colour Match (15% weight):** Clustered color taxonomy (e.g., Space Grey / Slate / Metallic).
  3. **Brand Overlap (15% weight):** Normalized fuzzy brand tokens.
  4. **Description Keywords (15% weight):** N-gram & keyword intersection.
  5. **Campus Zone Proximity (10% weight):** Evaluates building/quadrant proximity.
  6. **Time Decay Window (10% weight):** Highest score within hours, smoothly decaying.
- **Confidence Badges:** **HIGH (>=75%)**, **MEDIUM (45-74%)**, **LOW (<45%)**.
- **Admin Tuning:** Campus admins can tune weights and thresholds without changing a line of code via the dashboard.
- **User Feedback Loop:** Users can dismiss false positives with "Not Mine" (MT-7).

### 3. Anti-Fraud Claims & OTP Handover (CL-1 to CL-5)
- **Secret Verification Questions:** Finders or desk staff set a secret question only the rightful owner knows (e.g. "What sticker is on the palmrest?" or "What is the lock screen image?").
- **Handover OTP:** Once verification passes, the claimant receives a secure 6-digit numeric OTP code.
- **Physical Handover Release:** The finder or Security Desk enters the OTP code into their terminal to confirm identity, close both reports, and record an immutable audit log.
- **High-Value Protection:** Laptops, wallets, and smartphones require campus physical ID check by security desk staff.

### 4. Anonymous In-App Messenger & Safety (NT-1 to NT-5)
- Owners and finders can chat using masked pseudonyms ("Anonymous Owner" vs "Finder (Guest)").
- Pinned campus safety instructions advising meetups at the security desk.
- Report/flag message mechanism for abusive content (NT-5).

### 5. Security Desk & Admin Analytics (AD-1 to AD-6, Flow E)
- **Intake Terminal:** Quickly log physically handed-in items and assign physical lockers/shelves (e.g. `Locker Shelf A-14`).
- **Handover Terminal:** Enter 6-digit OTP code to release items.
- **Analytics KPIs:** Recovery rate percentage, median time to match tagged vs untagged, and median time to handover.
- **Campus Hotspots:** Live breakdown of campus areas with highest lost item incidence (e.g. Canteen, Library 2nd Floor).
- **Public Found Gallery (`/api/public/gallery`):** Public browsing with automated blur protection for sensitive ID cards and wallets (SR-1, SR-2).

---

## 🚀 Quick Start Guide

### 1. Requirements
- Python 3.10+ (Python 3.14+ supported)
- Standard modern web browser (Chrome, Safari, Edge, Firefox)

### 2. Start the Server
Run the application launcher:
```powershell
python run.py
```
Or directly via Uvicorn:
```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Access Everything From a Single Link
Open your browser to:
### 👉 **[http://localhost:8000](http://localhost:8000)**

You do **not** need any other URLs. From this single dashboard, you can:
- **My Tags:** View registered belongings, download QR tags, and 1-click toggle "Report Lost".
- **Scan & Finder View:** Camera QR scanner + interactive in-app zero-install Finder Simulator with one-click tests for tagged belongings.
- **Report:** File Lost or Found reports with campus location pickers and anti-fraud verification questions.
- **Instant Matches:** View real-time match rankings, score breakdowns, "This is Mine" claim buttons, and secure 6-digit Handover OTPs.
- **Public Gallery:** Browse campus found items with privacy blur for student ID cards and sensitive belongings.
- **Desk & Admin:** Security desk rapid custody intake, OTP verification release terminal, campus hotspot analytics, and algorithm weight tuning sliders.
- **Print Tags:** Full printable sticker sheet with cut guides and high-resolution QR codes, ready to print with one click (`window.print()`).
- **Anonymous Chat:** Direct anonymous masked messenger with safety warnings.

---

## 🧪 Testing All Flows

Run the automated test suite:
```powershell
python test_app.py
```
Every single flow (Registration -> Scan -> Instant Match -> Verification -> Handover OTP -> Analytics) is verified end-to-end.

---

## 👥 Persona Simulation

Use the **Persona Switcher** in the top navigation bar to test all user roles:
- **Sanis Sharma (Student/Owner):** View registered tags, mark items as lost, answer verification questions, view handover OTP.
- **Guest Finder:** Report an untagged found item with instant OTP verification.
- **Officer Rajesh Verma (Security Desk):** Intake physically received items into lockers, enter OTP to complete handover.
- **Dr. Anita Rao (Campus Admin):** Review analytics, adjust match algorithm weights, review audit logs.
