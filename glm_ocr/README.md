# GLM OCR 

Extract text from PDFs using a local GLM model via Ollama.

---

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com) installed and running

---

## Setup

### 1. Install Ollama

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS (Homebrew)
brew install ollama
```

> Windows: Download the installer from [ollama.com/download](https://ollama.com/download)

### 2. Pull the GLM OCR model

```bash
ollama pull glm-ocr
```

### 3. Start Ollama (if not already running)

```bash
ollama serve
```

### 4. Install Python dependency

```bash
pip install glmocr
```

---

## Usage

Update the file path in `glm.py`, then run:

```python
from glmocr import GlmOcr

with GlmOcr(config_path="config.yaml") as parser:
    result = parser.parse("/path/to/your/file.pdf")
    print(result.markdown_result)
```

```bash
python glm.py
```

---

## Configuration (`config.yaml`)

| Key | Value | Description |
|-----|-------|-------------|
| `api_host` | `localhost` | Ollama host |
| `api_port` | `11434` | Default Ollama port |
| `model` | `glm-ocr:latest` | Model to use |
| `api_mode` | `ollama_generate` | Use Ollama native format |
| `enable_layout` | `false` | Disable layout analysis (faster) |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `Connection refused` | Run `ollama serve` |
| Model not found | Run `ollama pull glm-ocr` |
| Slow processing | Keep `enable_layout: false` |
