# Document OCR & Extractor

A pipeline that extracts structured data from scanned documents — PDFs or images — using a two-stage approach: OCR to read the raw content, and an LLM to clean and structure it into JSON.

Useful for automating data entry from passports, resumes, invoices, bank statements, or any form-based document.

---

## How it works

1. **OCR** — EasyOCR handles printed text. If confidence is low (e.g. handwritten fields), it falls back to TrOCR (`trocr-large-printed`) for better accuracy. Native text is extracted directly from digital PDFs without OCR.
2. **Date normalization** — A post-processing step corrects common OCR misreads in date strings (e.g. `l5/O8/1998` → `15/08/1998`).
3. **LLM Chain** — The extracted text is passed through a 3-step Groq (Llama 3.1) chain: simplify → extract fields → output structured JSON.
4. **Output** — Returns document type + all detected fields as a clean JSON object.

---

## Requirements

- Python 3.9+
- A [Groq API key](https://console.groq.com) (free tier available)
- For GPU acceleration: a CUDA-compatible GPU or Apple Silicon (MPS). CPU works too, but is slower for TrOCR.

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

**2. Install dependencies**
```bash
pip install easyocr pymupdf pillow opencv-python flask groq python-dotenv transformers torch torchvision
```

> On Apple Silicon, PyTorch will automatically use MPS. For CUDA, make sure you install the correct torch version for your CUDA version from [pytorch.org](https://pytorch.org).

**3. Set up your API key**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_key_here
```
This is loaded automatically via `python-dotenv`. Never commit this file — add `.env` to your `.gitignore`.

**4. (First run only)** TrOCR weights (~1.3 GB) will be downloaded automatically from HuggingFace on first use.

---

## Usage

**Web UI** — upload a file and see results in the browser
```bash
python app.py
# Visit http://localhost:5001
```

**CLI** — full pipeline, prints extracted JSON
```bash
python main.py /path/to/document.pdf
```

**OCR only** — just extract raw text, no LLM
```bash
python run_ocr.py /path/to/document.pdf
```

---

## Supported formats

`.pdf` · `.png` · `.jpg` · `.jpeg`

---

## Output shape

```json
{
  "document_type": "Passport",
  "extracted_data": {
    "name": "Jane Doe",
    "date_of_birth": "15/08/1990",
    "address": "...",
    "email": "...",
    "phone": "..."
  }
}
```

Fields vary depending on the document type. The LLM extracts whatever is present.

---

## Project structure

```
├── app.py          # Flask web app
├── main.py         # CLI entrypoint (OCR + LLM chain)
├── run_ocr.py      # CLI entrypoint (OCR only)
├── utils.py        # OCR engine, LLM calls, helper functions
└── .env            # API keys (not committed)
```
