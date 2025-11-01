# 🚀 Quick Usage Guide

## ✅ Setup Complete!

Your installation is complete and verified. Everything is working correctly!

---

## 📄 Sample Test Deck Created

I've created a complete 14-slide pitch deck for you: **`sample_deck.pdf`**

This deck includes:
- Company overview (Acme Robotics)
- Problem statement
- Solution
- Product details
- Traction
- Team
- Market opportunity
- Business model
- Competition
- Moat
- Financials
- The ask
- Risks

---

## 🎯 How to Use the Tool

### **Option 1: Fast Mode (No API Credits Used)**
Quick text extraction without AI analysis:

```bash
python main.py sample_deck.pdf --fast
```

**Output:** Basic extraction summary (~0.5 seconds)

### **Option 2: Full AI Analysis (Uses OpenRouter API)**
Complete analysis with AI enrichment:

```bash
python main.py sample_deck.pdf
```

**Output:** Structured investment brief with detailed sections (~13 seconds)

### **Option 3: Debug Mode**
See the raw extracted text:

```bash
python main.py sample_deck.pdf --debug
```

### **Option 4: Custom Output Directory**
Save to a specific location:

```bash
python main.py sample_deck.pdf --output-dir my_briefs
```

---

## 📊 What You Get

### Fast Mode Output:
- Slide count
- Character count
- Basic extraction info
- **No AI analysis**

### Full AI Mode Output:
- **🧩 Problem**: What challenge the company addresses
- **🚀 Solution**: Their product/service offering
- **📈 Traction**: Metrics, customers, revenue
- **👥 Team**: Key people and backgrounds
- **🌍 Market**: TAM/SAM/SOM, growth rate
- **🧱 Moat**: Competitive advantages
- **⚠️ Risks**: Key challenges identified
- **📚 Sources**: Which slides info came from

---

## 📁 Your Test Results

I just analyzed the sample deck for you:

**Fast Mode:**
- Location: `./test_output/Acme_Robotics_Brief.md`
- Time: 0.5 seconds
- Result: Basic extraction

**Full AI Mode:**
- Location: `./test_output/Acme_Robotics_Brief_20251031_164052.md`
- Time: 13.3 seconds
- Result: Complete structured analysis

---

## 🎨 Try With Your Own Decks

### Supported Formats:
- ✅ `.pdf` - Any PDF file
- ✅ `.pptx` - PowerPoint files (2007+)
- ❌ `.ppt` - Old PowerPoint (convert to .pptx first)

### Best Practices:
1. **Start with --fast mode** to verify extraction works
2. **Use --debug mode** if text looks wrong
3. **Use full mode** when ready for detailed analysis
4. **10-50 slides** works best
5. **Text-based slides** extract better than image-heavy ones

---

## 🔑 Commands Reference

```bash
# Basic analysis
python main.py deck.pdf

# Fast mode (no API)
python main.py deck.pdf --fast

# Debug mode
python main.py deck.pdf --debug

# Custom output location
python main.py deck.pdf --output-dir my_folder

# Combined flags
python main.py deck.pdf --fast --debug --output-dir test

# Show help
python main.py --help
```

---

## 💡 Common Workflows

### Testing a New Deck:
```bash
# 1. Quick test with fast mode
python main.py new_deck.pdf --fast --debug

# 2. Check output looks reasonable
cat output/Company_Name_Brief.md

# 3. Run full analysis
python main.py new_deck.pdf
```

### Processing Multiple Decks:
```bash
python main.py deck1.pdf --output-dir batch1
python main.py deck2.pdf --output-dir batch1
python main.py deck3.pdf --output-dir batch1
```

### Troubleshooting:
```bash
# See what text was extracted
python main.py problem_deck.pdf --fast --debug

# Check the debug folder
ls -la debug/
cat debug/extraction_*.txt
```

---

## 🎯 Where to Find Real Pitch Decks

### Public Examples:
- **Airbnb's original pitch deck**
- **Uber's first pitch deck**
- **Dropbox's seed deck**
- Search: "YC startup pitch deck PDF"

### Repositories:
- SlideShare: pitch deck collections
- YC Library: startup resources
- Sequoia Capital: business plan templates

### Create Your Own:
Use the included script:
```bash
python create_test_deck.py
```

---

## 📈 Cost Estimation

### Fast Mode:
- **Free** - No API calls

### Full AI Mode (OpenRouter):
- ~$0.02-0.05 per deck
- Depends on deck size
- Claude 3.5 Sonnet pricing

---

## ⚠️ Important Notes

1. **Activate venv**: Your dependencies are in the virtual environment
   ```bash
   # If you open a new terminal, activate venv first:
   source venv/bin/activate
   ```

2. **API Key**: Already configured in `.env` file

3. **Tesseract OCR**: Already installed and working

4. **Output Location**: 
   - Default: `./output/`
   - Custom: Use `--output-dir` flag

---

## 🎓 Example Session

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run verification (optional)
python verify_setup.py

# Analyze the sample deck
python main.py sample_deck.pdf

# View the result
cat output/Acme_Robotics_Brief*.md

# Try with your own deck
python main.py ~/Downloads/my_pitch.pdf
```

---

## 🆘 Need Help?

### Check Setup:
```bash
python verify_setup.py
```

### Common Issues:

**"No module named 'click'"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**"Invalid API key"**
- Check `.env` file has your OpenRouter key

**"No text extracted"**
```bash
python main.py deck.pdf --debug
# Check debug/extraction_*.txt files
```

---

## 🎉 You're All Set!

Your PitchDeck Autopilot is ready to use. Start analyzing decks and creating investment briefs!

```bash
python main.py sample_deck.pdf
```

**Happy analyzing!** 🚀


