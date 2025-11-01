# 🔧 Installation Instructions

## Prerequisites Check

Before installing, verify you have:

1. **Python 3.10 or higher**
   ```bash
   python3 --version
   ```
   Should show: `Python 3.10.x` or higher

2. **pip (Python package manager)**
   ```bash
   pip --version
   ```

---

## Installation Steps

### Step 1: Install Python Dependencies

From the project root directory:

```bash
pip install -r requirements.txt
```

This will install all required packages:
- click (CLI framework)
- rich (terminal styling)
- pdfplumber (PDF parsing)
- python-pptx (PowerPoint parsing)
- pytesseract (OCR)
- Pillow (image processing)
- requests (HTTP client)
- python-dotenv (environment variables)

### Step 2: Install Tesseract OCR

Tesseract is required for OCR functionality (extracting text from image-based PDFs).

#### macOS
```bash
brew install tesseract
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### Windows
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer
3. Add Tesseract to your PATH

#### Verify Installation
```bash
tesseract --version
```

### Step 3: Install LibreOffice (Optional - for image-only PPTX decks)

LibreOffice is used to automatically convert image-only PPTX files to PDF for better OCR extraction. This is optional but highly recommended if you work with pitch decks that have text embedded in images.

#### macOS
```bash
brew install libreoffice
```

#### Ubuntu/Debian
```bash
sudo apt-get install libreoffice
```

#### Windows
Download and install from: https://www.libreoffice.org/download/download/

**Note:** If LibreOffice is not installed, image-only PPTX files will extract with minimal content. Text-based PPTX files work fine without it.

### Step 4: Configure OpenRouter API Key

1. **Get your API key**:
   - Visit: https://openrouter.ai/keys
   - Sign up (free tier available)
   - Copy your API key

2. **Create .env file**:
   ```bash
   cp .env.example .env
   ```

3. **Edit .env** and add your key:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
   ```

### Step 5: Verify Setup

Run the verification script:

```bash
python verify_setup.py
```

This will check:
- ✅ Python version
- ✅ All dependencies installed
- ✅ Tesseract OCR available
- ✅ .env file configured
- ✅ Project structure complete

---

## Quick Test

Once installed, test with:

```bash
python main.py --help
```

You should see:

```
Usage: main.py [OPTIONS] FILE_PATH

  Transform pitch decks into structured investment briefs.

  FILE_PATH: Path to the pitch deck (.pdf or .pptx)

Options:
  --fast         Skip AI enrichment, fast extraction only
  --debug        Show raw extracted text and save debug files
  --output-dir   Output directory for markdown files
  --help         Show this message and exit.
```

---

## Troubleshooting

### "No module named 'click'" (or other packages)
**Solution:** Run `pip install -r requirements.txt`

### "tesseract not found"
**Solution:** Install Tesseract OCR (see Step 2)

### "Invalid OpenRouter API key"
**Solution:** 
1. Check `.env` file exists
2. Verify API key is correct (starts with `sk-or-v1-`)
3. Ensure no quotes around the key in `.env`

### "Permission denied"
**Solution:** Make scripts executable:
```bash
chmod +x main.py verify_setup.py
```

### Import errors after installation
**Solution:** You might be using the wrong Python interpreter. Try:
```bash
python3 -m pip install -r requirements.txt
python3 main.py --help
```

---

## Alternative: Virtual Environment (Recommended)

For a clean installation, use a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the tool
python main.py --help
```

When done, deactivate:
```bash
deactivate
```

---

## System Requirements

### Minimum
- Python 3.10+
- 2 GB RAM
- 100 MB disk space

### Recommended
- Python 3.11+
- 4 GB RAM
- Tesseract OCR installed

### Internet Connection
Required for:
- Installing dependencies (pip)
- OpenRouter API calls (unless using --fast mode)

---

## Next Steps

After successful installation:

1. Read the [QUICKSTART.md](QUICKSTART.md) for your first analysis
2. Check [README.md](README.md) for complete documentation
3. Try running with a sample PDF:
   ```bash
   python main.py path/to/your/deck.pdf
   ```

---

## Support

If you encounter issues:

1. Run `python verify_setup.py` to diagnose problems
2. Check error messages (they're designed to be helpful!)
3. Use `--debug` flag for detailed output
4. Review the [README.md](README.md) troubleshooting section

---

**Happy deck analyzing!** 🚀

