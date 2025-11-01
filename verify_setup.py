#!/usr/bin/env python3
"""
Setup verification script for PitchDeck Autopilot.
Run this to check if everything is configured correctly.
"""

import sys
import os
from importlib import util

def check_python_version():
    """Check if Python version is 3.10+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected (3.10+ required)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} detected - need 3.10+")
        return False


def check_package(package_name):
    """Check if a Python package is installed"""
    spec = util.find_spec(package_name)
    if spec is not None:
        print(f"✅ {package_name} installed")
        return True
    else:
        print(f"❌ {package_name} not installed")
        return False


def check_tesseract():
    """Check if Tesseract OCR is installed"""
    import shutil
    if shutil.which("tesseract"):
        print("✅ Tesseract OCR installed")
        return True
    else:
        print("⚠️  Tesseract OCR not found (optional, but recommended)")
        return True  # Don't fail on this


def check_env_file():
    """Check if .env file exists and has API key"""
    if os.path.exists(".env"):
        print("✅ .env file exists")
        
        # Check if API key is set
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        
        if api_key and api_key != "your_api_key_here":
            print("✅ OPENROUTER_API_KEY is configured")
            return True
        else:
            print("⚠️  OPENROUTER_API_KEY not set in .env file")
            print("   Get your key from: https://openrouter.ai/keys")
            return False
    else:
        print("⚠️  .env file not found")
        print("   Run: cp .env.example .env")
        print("   Then add your OpenRouter API key")
        return False


def check_project_structure():
    """Check if all required files exist"""
    required_files = [
        "main.py",
        "deckbrief/__init__.py",
        "deckbrief/deck_parser.py",
        "deckbrief/text_cleaner.py",
        "deckbrief/ai_analyzer.py",
        "deckbrief/markdown_builder.py",
        "deckbrief/cli_ui.py",
        "requirements.txt",
        "README.md",
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            pass  # Don't print each file, too verbose
        else:
            print(f"❌ Missing file: {file}")
            all_exist = False
    
    if all_exist:
        print("✅ Project structure complete")
    
    return all_exist


def main():
    """Run all verification checks"""
    print("🔍 PitchDeck Autopilot - Setup Verification")
    print("─" * 50)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Project Structure", check_project_structure),
        ("click", lambda: check_package("click")),
        ("rich", lambda: check_package("rich")),
        ("pdfplumber", lambda: check_package("pdfplumber")),
        ("pptx", lambda: check_package("pptx")),
        ("pytesseract", lambda: check_package("pytesseract")),
        ("PIL", lambda: check_package("PIL")),
        ("requests", lambda: check_package("requests")),
        ("dotenv", lambda: check_package("dotenv")),
        ("Tesseract OCR", check_tesseract),
        ("Environment Config", check_env_file),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")
            results.append((name, False))
    
    print()
    print("─" * 50)
    print("📊 Summary")
    print("─" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Passed: {passed}/{total} checks")
    print()
    
    if passed == total:
        print("✅ All checks passed! You're ready to go.")
        print()
        print("Try running:")
        print("  python main.py --help")
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print()
        print("Common fixes:")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("  • Create .env file: cp .env.example .env")
        print("  • Add OpenRouter key to .env")
        print("  • Install Tesseract: brew install tesseract (macOS)")


if __name__ == "__main__":
    main()

