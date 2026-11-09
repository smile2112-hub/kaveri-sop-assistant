# Kaveri Plant Copilot

Small FastAPI + browser UI assignment for BiztelAI. The copilot searches the supplied Kaveri Precision Components maintenance, quality, and safety procedures and returns the matching document excerpt and source filename. It does not invent an answer when the documents do not contain one.

## What is included

- `app.py` - FastAPI API and a small, explainable retrieval layer.
- `static/` - responsive UI designed for a phone or tablet.
- `documents/` - the three supplied document sets captured as text source files:
  - `01_loto_safety.txt`
  - `02_incoming_inspection.txt` (Revision 04, which supersedes Revision 03)
  - `03_tx200_maintenance.txt`
- `tests/` - focused retrieval tests.
- `run.ps1` - one-command Windows startup helper.

The original PDF attachments were not available in the working folder when this was built. The source content supplied in the assignment prompt is preserved as text so the submission remains runnable. The loader also accepts `.pdf` files in `documents/` using `pypdf`; replacing the text files with the original PDFs does not require code changes.

## Run locally

Requires Python 3.10+.

```powershell
cd "C:\Users\Uday\Desktop\Company Coding Tasks\Biztelal Technology"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Open <http://127.0.0.1:8000>. The API is also available at `/api/ask?question=...` and health is at `/api/health`.

## Use it from a phone on the same Wi-Fi

1. Find the laptop's private IPv4 address with `ipconfig` (for example, `192.168.1.23`).
2. Start the server on all interfaces:

   ```powershell
   python -m uvicorn app:app --host 0.0.0.0 --port 8000
   ```

3. If Windows Firewall prompts, allow Python on the **Private networks** profile, or add a narrowly scoped inbound TCP rule for port 8000.
4. On the phone, connected to the same Wi-Fi, open `http://192.168.1.23:8000`.

The phone must be on the same local network; `127.0.0.1` on the phone means the phone itself.

## Tests

```powershell
python -m pytest -q tests
```

If `python` is not on PATH on Windows, use the Python launcher instead:

```powershell
py -m pytest -q tests
```

## Project structure

```text
Biztelal Technology/
├── app.py
├── documents/
│   ├── 01_loto_safety.txt
│   ├── 02_incoming_inspection.txt
│   └── 03_tx200_maintenance.txt
├── static/
│   ├── index.html
│   └── styles.css
├── tests/test_app.py
├── requirements.txt
├── run.ps1
├── README.md
└── THINKING.md
```

## Quick start with the helper

After dependencies are installed, run:

```powershell
.\run.ps1
```

For phone access:

```powershell
.\run.ps1 -Network
```

## Sample question checks

These are the expected answers from the current source documents:

| Question | App answer |
|---|---|
| What is the recommended coolant concentration for the TX-200 CNC turning centre? | **6–8 percent**, measured with a refractometer using factor 1.0. Source: `03_tx200_maintenance.txt`. |
| The machine is showing alarm AL-104. What does it mean and what should the operator do? | **Way lube oil level low.** Top up with ISO VG 68 oil to MAX, then press RESET; the machine can continue after reset. Source: `03_tx200_maintenance.txt`. |
| Who is allowed to remove a lockout lock from a machine? | Each authorised person removes **only their own lock**. Nobody may remove another person's lock. The absent-owner exception requires the Shift Supervisor's contact attempt and joint Production Manager + Safety Officer authorisation. Source: `01_loto_safety.txt`. |
| What is the outer diameter tolerance for the BH-220 bearing housing? | **90.000 +/- 0.050 mm**, checked with a digital caliper. Source: `02_incoming_inspection.txt`. |
| How often should spindle runout be checked, and who does it? | **Monthly**, by a **maintenance technician**. The limit is 0.005 mm maximum at the chuck face. Source: `03_tx200_maintenance.txt`. |

## Five additional questions

| Question | App answer |
|---|---|
| What must happen if the supplier Material Test Certificate is missing? | Put the lot on **HOLD**; it must not be inspected or accepted until the MTC arrives. Source: `02_incoming_inspection.txt`. |
| Where should a rejected incoming lot be stored? | In locked **Quarantine Cage Q1, Stores Bay 3**; the Shift QC Supervisor holds the key. Source: `02_incoming_inspection.txt`. |
| What does AL-305 mean? | **Spindle overload.** Stop the cycle, check tool wear and cutting parameters, and inform the shift supervisor. Source: `03_tx200_maintenance.txt`. |
| How frequently are LOTO refreshers required? | Every **12 months** for authorised persons. Source: `01_loto_safety.txt`. |
| What is the cafeteria menu on Friday? | **Not found in the plant documents.** The app says it cannot answer instead of guessing and shows no source. |






## Design note

The retrieval implementation is intentionally small and inspectable for this assignment: it tokenizes paragraphs, ranks them by query-term overlap, and applies a conservative threshold. This is not a production-grade semantic RAG system. A production version should use a proper embedding index, document version/ACL filtering, audit logging, and a model constrained to retrieved passages. See [THINKING.md](./THINKING.md) for the user journey, critique, chosen improvement, and open questions.






Live Demo Link
https://drive.google.com/file/d/1hPKiSK7TZVCgCesXdcz_C0Ck2cL0F2gK/view?usp=drive_link
