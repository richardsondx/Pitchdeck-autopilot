"""
Setup configuration for PitchDeck Autopilot.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pitchdeck-autopilot",
    version="1.0.0",
    author="PitchDeck Autopilot Team",
    description="Transform pitch decks into structured investment briefs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pitchdeck-autopilot/deckbrief",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "click>=8.1.7",
        "rich>=13.7.0",
        "pdfplumber>=0.11.0",
        "python-pptx>=0.6.23",
        "pytesseract>=0.3.10",
        "Pillow>=10.0.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "deckbrief=main:cli",
        ],
    },
)

