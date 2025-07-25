# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python tool for generating A4 word grids from wordlists with numbered images using Jinja2 templates and WeasyPrint. Creates print-ready PDFs with 4×8 grids (32 words per page) for vocabulary cards, language learning, or BIP39 seed phrase references.

## Core Architecture

### Main Components

- **jinja_weasyprint_solution.py** - Main word grid generator with CLI interface
- **main.py** - Simple standalone generator (legacy/demo version)  
- **wordlist_setup_script.py** - Setup utility for creating sample data and testing

### Key Classes

- **WordGridGenerator** - Core class handling PDF generation, image processing, and template rendering
  - `generate_pdf()` - Single wordlist processing
  - `generate_all_wordlists()` - Batch processing
  - `generate_combined_pdf()` - Multiple wordlists into single PDF
  - `find_wordlists()` - Auto-discovery of wordlist files and image directories

### Template System

Uses Jinja2 HTML template with embedded CSS for A4 print formatting. Template supports:
- 4×8 grid layout with precise margins for printing
- Base64 embedded images for standalone PDFs
- Fallback placeholder images when no image files found
- Responsive typography and modern styling

## Development Commands

### Setup and Dependencies
```bash
# Install required packages
pip install jinja2 weasyprint pillow

# Create sample wordlist structure and test
python wordlist_setup_script.py --all

# Install ImageMagick for placeholder image generation (optional)
# macOS: brew install imagemagick
# Ubuntu: sudo apt-get install imagemagick
```

### Primary Usage
```bash
# Process all wordlists in wordlists/ directory
python jinja_weasyprint_solution.py --all

# Process specific wordlist with images
python jinja_weasyprint_solution.py --wordlist wordlists/001.txt --images wordlists/001

# Generate combined PDF from all wordlists  
python jinja_weasyprint_solution.py --combined

# Custom output directory and title
python jinja_weasyprint_solution.py --all --output my_pdfs --title "My Vocabulary Cards"
```

### Testing and Setup
```bash
# Create sample data and run tests
python wordlist_setup_script.py --all

# Just create sample wordlists
python wordlist_setup_script.py --create-samples

# Test generator with existing data
python wordlist_setup_script.py --test
```

## Directory Structure Requirements

The tool expects a specific directory structure for wordlists and images:

```
wordlists/
├── 001.txt              # First wordlist (one word per line)
├── 001/                 # Images for first wordlist  
│   ├── 001.png          # Image for 1st word in 001.txt
│   ├── 002.png          # Image for 2nd word in 001.txt
│   └── ...              # Up to 032.png
├── 002.txt              # Second wordlist
├── 002/                 # Images for second wordlist
└── ...
```

### Image Conventions

- **Naming**: Numbered sequentially (001.png, 002.png, etc.)
- **Formats**: PNG, JPG, JPEG supported
- **Position Matching**: Image 001.png corresponds to 1st word, 002.png to 2nd word
- **Fallback**: Generator works without images, shows placeholder blocks

## Output Structure

Generated files go to `output/` directory (configurable):
- `wordlist_001.pdf` - Final PDF for printing
- `wordlist_001.html` - HTML preview for debugging
- `combined_wordlists.pdf` - Combined PDF when using --combined

## Key Technical Details

### PDF Generation Pipeline
1. Load wordlist file (UTF-8 encoding)
2. Auto-discover corresponding image directory  
3. Match images by number (001.png → word 1)
4. Embed images as base64 in HTML template
5. Render to PDF using WeasyPrint with A4 page settings
6. Generate debug HTML file alongside PDF

### Image Processing
- Converts images to base64 for embedding
- Handles multiple formats (PNG/JPG/JPEG)
- Falls back gracefully when images missing
- Automatically resizes to fit grid cells

### Error Handling
- Graceful degradation when images/directories missing
- UTF-8 encoding handling for international wordlists
- Validation of file formats and directory structure
- Detailed error messages for troubleshooting