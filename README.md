# Wordlist Word Grid Generator

A modern Python solution for generating A4 word grids from multiple wordlists with numbered images using Jinja2 templates and WeasyPrint.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install jinja2 weasyprint pillow
```

### 2. Setup Sample Data
```bash
# Create sample wordlist structure and test
python wordlist_setup.py --all
```

### 3. Generate Word Grids
```bash
# Process all wordlists
python word_grid_generator.py --all

# Generate combined PDF
python word_grid_generator.py --combined
```

## 📁 Directory Structure

Your wordlists should follow this structure:

```
wordlists/
├── 001.txt          # First wordlist (one word per line)
├── 001/             # Images for first wordlist
│   ├── 001.png      # Image for 1st word in 001.txt
│   ├── 002.png      # Image for 2nd word in 001.txt
│   ├── 003.png      # Image for 3rd word in 001.txt
│   └── ...          # Up to 032.png
├── 002.txt          # Second wordlist
├── 002/             # Images for second wordlist
│   ├── 001.png      # Image for 1st word in 002.txt
│   ├── 002.png      # Image for 2nd word in 002.txt
│   └── ...
└── 003.txt          # Third wordlist
    ├── 003/         # Images for third wordlist
    └── ...
```

## 🎯 Usage Examples

### Process All Wordlists
```bash
# Basic usage - processes all .txt files in wordlists/
python word_grid_generator.py --all

# Custom output directory
python word_grid_generator.py --all --output my_pdfs

# Custom title
python word_grid_generator.py --all --title "My Vocabulary Cards"
```

### Process Specific Wordlist
```bash
# Single wordlist with images
python word_grid_generator.py \
  --wordlist wordlists/001.txt \
  --images wordlists/001

# Without images
python word_grid_generator.py \
  --wordlist wordlists/001.txt \
  --images wordlists/nonexistent
```

### Generate Combined PDF
```bash
# Combine all wordlists into single PDF
python word_grid_generator.py --combined

# Combined with custom settings
python word_grid_generator.py \
  --combined \
  --wordlists-dir my_wordlists \
  --output combined_output.pdf \
  --title "Complete Vocabulary"
```

## 🖼️ Image Requirements

- **Format**: PNG, JPG, or JPEG
- **Naming**: Must be numbered sequentially (`001.png`, `002.png`, etc.)
- **Size**: Any size (automatically resized to fit grid cells)
- **Position**: Image `001.png` corresponds to 1st word, `002.png` to 2nd word, etc.

## 📋 Features

- ✅ **A4 Print Format**: Precise margins and sizing for printing
- ✅ **4×8 Grid Layout**: 32 words per page
- ✅ **Multiple Wordlists**: Process multiple wordlists automatically
- ✅ **Numbered Images**: Images matched by position (001.png, 002.png, etc.)
- ✅ **Fallback Support**: Works with or without images
- ✅ **Modern Typography**: Clean, professional layout
- ✅ **Batch Processing**: Generate multiple PDFs at once
- ✅ **Combined Output**: Merge multiple wordlists into single PDF
- ✅ **HTML Preview**: Debug HTML files generated alongside PDFs

## 🛠️ Advanced Options

### Command Line Options
```bash
python word_grid_generator.py --help
```

Key options:
- `--wordlists-dir`: Directory containing wordlists (default: `wordlists`)
- `--output`: Output directory for PDFs (default: `output`)
- `--title`: Title for the word grids
- `--all`: Process all wordlists
- `--combined`: Generate single combined PDF
- `--wordlist`: Process specific wordlist file
- `--images`: Images directory (for single wordlist mode)

### Example Wordlist File (`001.txt`)
```
Apple
Banana
Cherry
Date
Elderberry
Fig
Grape
Honeydew
Kiwi
Lemon
Mango
Orange
Papaya
Quince
Raspberry
Strawberry
```

## 🎨 Customization

The generator uses Jinja2 templates, so you can customize:

1. **Layout**: Modify the CSS grid in the HTML template
2. **Styling**: Change colors, fonts, spacing in the CSS
3. **Content**: Adjust how words and images are displayed
4. **Page Size**: Change from A4 to other formats

## 🐛 Troubleshooting

### Common Issues

**No images found:**
- Check image directory exists and matches wordlist number
- Verify image naming (001.png, 002.png, etc.)
- Supported formats: PNG, JPG, JPEG

**Empty PDFs:**
- Check wordlist files contain words (one per line)
- Verify file encoding is UTF-8
- Ensure wordlist files end with `.txt`

**Import errors:**
- Install dependencies: `pip install jinja2 weasyprint pillow`
- On Linux: May need `sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0`

**ImageMagick warnings (setup script):**
- Install ImageMagick for placeholder image creation
- macOS: `brew install imagemagick`
- Ubuntu: `sudo apt-get install imagemagick`

### Debug Mode
The generator creates HTML files alongside PDFs for debugging:
- `wordlist_001.html` - Preview in browser
- Check console for detailed error messages

## 📝 File Outputs

For each wordlist, you get:
- `wordlist_001.pdf` - Final PDF for printing
- `wordlist_001.html` - HTML preview file
- `combined_wordlists.pdf` - Combined PDF (if using --combined)

## 🔧 Integration

This tool can be integrated into larger workflows:
- **Batch Processing**: Process hundreds of wordlists automatically
- **CI/CD**: Generate PDFs as part of automated builds
- **Educational Tools**: Create vocabulary cards for language learning
- **Print Shops**: Generate print-ready materials

## 📄 License

Free to use and modify. Based on modern web technologies (Jinja2 + WeasyPrint) for professional PDF generation.
