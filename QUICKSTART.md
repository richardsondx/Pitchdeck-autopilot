# 🚀 Quick Start Guide

Get up and running with PitchDeck Autopilot in 5 minutes.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Install Tesseract OCR

### macOS
```bash
brew install tesseract
```

### Ubuntu/Debian
```bash
sudo apt-get install tesseract-ocr
```

### Windows
Download from: https://github.com/UB-Mannheim/tesseract/wiki

## Step 3: Set Up API Key

1. Get your free API key from: https://openrouter.ai/keys

2. Create a `.env` file:
```bash
cp .env.example .env
```

3. Edit `.env` and add your key:
```
OPENROUTER_API_KEY=your_actual_key_here
```

## Step 4: Run Your First Analysis

```bash
python main.py path/to/your/deck.pdf
```

That's it! Check the `output/` directory for your Markdown brief.

## Example Commands

### Basic usage
```bash
python main.py pitch.pdf
```

### Fast mode (no AI)
```bash
python main.py pitch.pdf --fast
```

### Debug mode
```bash
python main.py pitch.pdf --debug
```

## Troubleshooting

### "No module named 'deckbrief'"
Run: `pip install -r requirements.txt`

### "Invalid OpenRouter API key"
Check your `.env` file has the correct key from OpenRouter.

### "tesseract not found"
Install Tesseract OCR (see Step 2 above)

### No text extracted
- Try with `--debug` flag to see raw extraction
- Ensure the PDF is not encrypted
- Check if PDF is image-based (OCR will activate automatically)

## What Gets Generated

After processing, you'll find a Markdown file in `output/` with:

- Company name and tagline
- Problem and solution sections
- Traction metrics
- Team information
- Market analysis
- Competitive moat
- Risk assessment
- Source references

Perfect for comparing multiple startups side-by-side!

