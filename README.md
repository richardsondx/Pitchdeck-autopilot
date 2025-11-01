# 🚀 PitchDeck Autopilot

**Transform messy startup pitch decks into well-structured Markdown investment briefs — in seconds.**

PitchDeck Autopilot is a command-line tool that automatically extracts, analyzes, and summarizes pitch decks (PDF/PPT) using AI, allowing investors to quickly compare companies in a standardized format.

---

## 🎯 What It Does

Give it a pitch deck → Get a structured investment brief.

- 📂 **Extracts content** from PDF and PPTX files (with OCR fallback)
- 🧹 **Cleans and normalizes** messy slide text
- 🧠 **AI-powered analysis** using Claude 3.5 Sonnet via OpenRouter
- 📄 **Generates beautiful Markdown** with standardized sections
- ⚡ **Premium CLI experience** with progress bars, colors, and polish

Perfect for busy investment associates, solo GPs, or anyone reviewing multiple startups.

---

## 🛠️ Installation

### Prerequisites

- **Python 3.10+** (check with `python3 --version`)
- **Tesseract OCR** (for image-heavy PDFs)

Install Tesseract:

```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### Setup

1. **Clone or download** this repository:

```bash
git clone https://github.com/pitchdeck-autopilot/deckbrief.git
cd deckbrief
```

2. **Install Python dependencies**:

```bash
pip install -r requirements.txt
```

3. **Configure your OpenRouter API key**:

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit `.env` and add your API key:

```
OPENROUTER_API_KEY=your_actual_key_here
```

Get your free API key from: [https://openrouter.ai/keys](https://openrouter.ai/keys)

---

## 🚀 Usage

### Basic Command

```bash
python main.py path/to/deck.pdf
```

### Examples

**Analyze a PDF deck:**
```bash
python main.py decks/startup_pitch.pdf
```

**Analyze a PowerPoint:**
```bash
python main.py presentations/company.pptx
```

**Fast mode** (skip AI, just extract text):
```bash
python main.py deck.pdf --fast
```

**Debug mode** (show raw extraction and save debug files):
```bash
python main.py deck.pdf --debug
```

**Custom output directory:**
```bash
python main.py deck.pdf --output-dir my_briefs
```

---

## 📊 Output Example

After processing, you'll get a structured Markdown file in the `output/` directory:

```markdown
# Company Brief: Acme Robotics

**Deck Parsed:** 32 slides  
**Generated:** 2024-01-15 14:30  
**Confidence:** 87%

---

**AI-native robotics platform trained on synthetic data**

---

### 🧩 Problem

Industrial robots remain siloed and require extensive real-world training data, making deployment slow and expensive.

### 🚀 Solution

Acme builds an AI-native robotics platform that uses synthetic data generation to train robot models 10x faster than traditional methods.

### 📈 Traction

- 2 pilot customers in automotive manufacturing
- $250K in committed ARR for 2025
- 15,000 hours of simulation data generated

### 👥 Team

Founded by ex-DeepMind engineers with PhDs in robotics from MIT and Stanford. 5-person team with combined 20 years in ML and robotics.

### 🌍 Market

$8.3B addressable market in industrial automation, growing at 19% CAGR. Target customers are mid-size manufacturers.

### 🧱 Moat

Proprietary synthetic data generation pipeline and simulation environment that competitors would take years to replicate.

### ⚠️ Risks

- High compute costs for training
- Hardware dependency for deployment
- Need to prove accuracy in real-world environments

---

### 📚 Sources

- Slide 3
- Slide 12-15
- Slide 28
```

---

## 💡 How It Works

The tool follows a 4-stage pipeline:

1. **🔍 Extract**: Parse PDF/PPTX files, using OCR for image-heavy slides
2. **🧹 Clean**: Remove headers/footers, normalize whitespace, merge fragments
3. **🧠 Analyze**: Send content to Claude 3.5 Sonnet for structured analysis
4. **📄 Generate**: Build formatted Markdown with emoji icons and metadata

Each stage provides visual feedback in the terminal with progress bars and status updates.

---

## ⚙️ Advanced Options

### Command-Line Flags

| Flag | Description |
|------|-------------|
| `--fast` | Skip AI enrichment, generate basic extraction summary only |
| `--debug` | Show raw extracted text and save debug files to `./debug/` |
| `--output-dir PATH` | Specify custom output directory (default: `./output/`) |
| `--help` | Show help message with all options |

### Environment Variables

Configure these in your `.env` file:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Yes (except in `--fast` mode) |

---

## 🎨 Terminal UX Features

This CLI is designed to *feel* like a product, not a script:

- ✨ **Colored output** (blue headers, green success, yellow warnings, red errors)
- 📊 **Progress bars** for long-running operations
- 🎯 **Unicode icons** for visual stage recognition
- ⏱️ **Elapsed time** tracking
- 🧱 **Dividers and formatting** for clean visual hierarchy

Example output:

```
🚀 PitchDeck Autopilot v1.0
────────────────────────────────────────────
📂 Input: decks/startup_pitch.pdf
🧠 Mode: Enriched (OpenRouter)
────────────────────────────────────────────

🔍 Extracting slides...
✅ 32 slides extracted (OCR used on 2 slides)

🧹 Cleaning text...
✅ Text cleaned and normalized

🧠 Analyzing content with OpenRouter...
✅ AI analysis complete

📄 Writing structured Markdown brief...
✅ Markdown brief generated

────────────────────────────────────────────
✅ Analysis complete!
📁 Output saved to: output/Acme_Robotics_Brief.md

⏱️  Total time: 1m 28s
────────────────────────────────────────────
```

---

## 🧪 Testing

To test the tool with a sample deck:

1. Place a PDF or PPTX file in the project directory
2. Run: `python main.py your_deck.pdf`
3. Check the `output/` directory for the generated Markdown

**Test cases:**
- ✅ PDF with 30+ slides
- ✅ PPTX presentation
- ✅ Invalid file path (should show error)
- ✅ `--fast` mode (no API call)
- ✅ `--debug` mode (raw output)

---

## 🔮 Future Enhancements

Potential features for future versions:

- 📦 **Batch mode**: Process multiple decks in one command
- 🎯 **Custom prompts**: User-defined analysis sections
- 🌐 **External Enrichment**: Add company data from sources like Crunchbase, TechCrunch, and patent databases to validate funding stage, founding year, and technology claims
- 👥 **Team Insights**: Include founder information even when missing in the deck (e.g., inferred from Crunchbase or LinkedIn)
- 🏷️ **Source Labels**: Tag each fact as `[Deck]`, `[Web]`, or `[AI Inference]` to improve transparency
- 📊 **Market Signals**: Auto-fetch comparable companies and recent funding news to enrich "Market" and "Moat" sections
- 🎯 **Confidence Scoring**: Display per-section confidence (e.g., Deck 100%, Web 85%, AI 70%) for quick trust assessment
- 🔒 **File Size Limits**: Add maximum file size check before processing to prevent resource exhaustion
- ⚡ **OCR Optimization**: Add per-page timeout and attempt limits for OCR processing to improve performance
- 🚦 **API Rate Limiting**: Implement rate limiting for API calls to prevent quota exhaustion and control costs
- 🧹 **Enhanced Cleanup**: Improve temporary file cleanup with automatic removal of stale files (pptx -> pdf temp files)

---

## 🛡️ Error Handling

The tool provides clear, friendly error messages:

| Error | Message |
|-------|---------|
| File not found | `❌ File not found: path/to/file.pdf` |
| Unsupported format | `❌ Unsupported file format: .doc. Only .pdf and .pptx are supported.` |
| No text extracted | `⚠️ No content could be extracted from the deck` |
| Invalid API key | `❌ Invalid OpenRouter API key. Please set OPENROUTER_API_KEY...` |
| API timeout | `❌ OpenRouter API request timed out after multiple retries` |

---

## 📋 Requirements

### Python Packages

```
click>=8.1.7
rich>=13.7.0
pdfplumber>=0.11.0
python-pptx>=0.6.23
pytesseract>=0.3.10
Pillow>=10.0.0
requests>=2.31.0
python-dotenv>=1.0.0
```

### System Requirements

- Python 3.10 or higher
- Tesseract OCR (for image-based PDFs)
- Internet connection (for OpenRouter API)

---

## 📝 File Structure

```
deckbrief/
├── main.py                    # CLI entry point
├── deckbrief/
│   ├── __init__.py           # Package initialization
│   ├── deck_parser.py        # PDF/PPT extraction logic
│   ├── text_cleaner.py       # Content normalization
│   ├── ai_analyzer.py        # OpenRouter API integration
│   ├── markdown_builder.py   # Output generation
│   └── cli_ui.py             # Progress bars, colors, styling
├── output/                   # Generated markdown briefs
├── .env                      # Your API key (not in git)
├── .env.example              # Template for API key
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🤝 Contributing

This project was built as a technical assessment demonstration. Feel free to fork and extend it!

Potential improvements:
- Add support for Google Slides
- Implement batch processing
- Create a web UI
- Add external enrichment from Crunchbase, TechCrunch, and patent databases
- Include founder information from LinkedIn and other sources
- Tag facts with source labels (`[Deck]`, `[Web]`, `[AI Inference]`)
- Auto-fetch comparable companies and recent funding news
- Display per-section confidence scores for transparency
- Add maximum file size check before processing (e.g., 50MB limit)
- Implement OCR resource management (timeouts per page, attempt limits)
- Add rate limiting for API calls to control costs and prevent quota exhaustion
- Improve temporary file cleanup with automatic stale file removal

---

## 📄 License

MIT License - feel free to use this code for your own projects.

---

## 💬 Support

For issues or questions:
- Check the `--debug` output for troubleshooting
- Review error messages (they're designed to be helpful!)
- Ensure your OpenRouter API key is valid
- Verify Tesseract is installed (`tesseract --version`)

---

## 🎯 Design Philosophy

This tool was built with three principles:

1. **Speed**: Process decks in under 2 minutes
2. **Polish**: Terminal UX should feel like a product, not a script
3. **Reliability**: Graceful error handling, clear feedback, no silent failures

The result is a CLI that *looks and feels professional* — not like a throwaway coding test.

---

**Made with ❤️ by Richardson Dackam for investors who value their time.**

