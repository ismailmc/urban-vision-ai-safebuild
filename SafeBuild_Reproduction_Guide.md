# SafeBuild Local Reproduction & Operational Verification Guide

**Urban Vision AI — SafeBuild**  
*“Plan roadwork. Keep communities connected.”*  
**Document Version:** 4.2.0  
**Target Environment:** Linux (Ubuntu 20.04+, Debian 11+, or compatible), Python 3.10+, Node.js 18+  

---

## 1. Prerequisites & System Requirements

* **Python:** 3.10, 3.11, or 3.12 (virtual environment recommended)
* **Node.js:** 18.x or 20.x LTS (`npm` 9.x+)
* **System Utilities:** `pdftoppm` (part of `poppler-utils`), `curl`
* **RAM & CPU:** Minimum 4 GB RAM, 2 CPU cores. No GPU required.

---

## 2. Quickstart Execution (Single Terminal Flow)

### Step 2.1: Clone & Configure Python Environment
```bash
# Clone the repository
git clone https://github.com/ismailmc/urban-vision-ai-safebuild.git
cd urban-vision-ai-safebuild

# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required backend dependencies
pip install fastapi uvicorn networkx pydantic reportlab
```

### Step 2.2: Configure Environment Variables
```bash
# Copy sanitized template
cp .env.example .env

# Note: GEMINI_API_KEY is completely optional. If omitted,
# SafeBuild automatically activates the deterministic grounded routing analyst.
```

### Step 2.3: Install & Build Frontend
```bash
cd frontend
npm install
npm run build
cd ..
```

---

## 3. Running Automated Validation Tests

SafeBuild includes an automated validation suite verifying all 17 analytical invariants, circular dependency detection, multi-phase calculations, and statutory gates:

```bash
# Run the complete test suite
./venv/bin/python3 -m unittest discover backend/tests
```

**Expected Test Output:**
```text
Ran 17 tests in ~12.2s

OK
```

---

## 4. Launching the Live Application

### Step 4.1: Launch Backend API Server (Port 8000)
```bash
./venv/bin/uvicorn backend.api.server:app --host 0.0.0.0 --port 8000
```
* Verify health endpoint: `curl -s http://localhost:8000/api/health`
* Interactive OpenAPI Documentation: `http://localhost:8000/docs`

### Step 4.2: Launch Frontend Web Interface (Port 3000)
In a second terminal:
```bash
cd frontend
npm start -p 3000
```
Open `http://localhost:3000/` in Google Chrome or any modern browser.

---

## 5. Re-generating Evidence Documents

To re-generate the official submission PDF evidence package:
```bash
./venv/bin/python3 scripts/generate_evidence_pdf.py
```
This produces `SafeBuild_Prototype_and_Test_Evidence.pdf` (8 readable pages, ~4.4 MB).

To render and visually inspect individual PDF pages:
```bash
pdftoppm -png -r 150 SafeBuild_Prototype_and_Test_Evidence.pdf evidence/pdf_page
```

To re-capture live screenshot evidence from the running interface:
```bash
node scripts/capture_evidence_screens.js
```
