# BIP39 Wordlist Print Generator

A Python tool for generating printable A4 word grids from BIP39 seed phrase wordlists. Creates professional PDFs with 4×8 grids (32 words per page) perfect for offline seed phrase references, recovery guides, or language learning materials.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install jinja2 weasyprint pillow
```

### 2. Setup Sample Data
```bash
# Create sample wordlist structure and test
python wordlist_setup_script.py --all
```

### 3. Generate Word Grids
```bash
# Process all wordlists
python jinja_weasyprint_solution.py --all

# Generate combined PDF
python jinja_weasyprint_solution.py --combined
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
python jinja_weasyprint_solution.py --all

# Custom output directory
python jinja_weasyprint_solution.py --all --output my_pdfs

# Custom title
python jinja_weasyprint_solution.py --all --title "BIP39 Reference Cards"
```

### Process Specific Wordlist
```bash
# Single wordlist with images
python jinja_weasyprint_solution.py \
  --wordlist wordlists/001.txt \
  --images wordlists/001

# Without images
python jinja_weasyprint_solution.py \
  --wordlist wordlists/001.txt \
  --images wordlists/nonexistent
```

### Generate Combined PDF
```bash
# Combine all wordlists into single PDF
python jinja_weasyprint_solution.py --combined

# Combined with custom settings
python jinja_weasyprint_solution.py \
  --combined \
  --wordlists-dir my_wordlists \
  --output combined_output.pdf \
  --title "Complete BIP39 Reference"
```

## 🖼️ Image Requirements

- **Format**: PNG, JPG, or JPEG
- **Naming**: Must be numbered sequentially (`001.png`, `002.png`, etc.)
- **Size**: Any size (automatically resized to fit grid cells)
- **Position**: Image `001.png` corresponds to 1st word, `002.png` to 2nd word, etc.

## 📋 Features

- ✅ **BIP39 Focused**: Optimized for cryptocurrency seed phrase wordlists
- ✅ **A4 Print Format**: Precise margins and sizing for offline storage
- ✅ **4×8 Grid Layout**: 32 words per page for complete reference
- ✅ **Multiple Languages**: Process BIP39 wordlists in 10+ languages
- ✅ **Numbered Images**: Optional visual mnemonics (001.png, 002.png, etc.)
- ✅ **Offline Reference**: Self-contained PDFs for secure storage
- ✅ **Batch Processing**: Generate multiple PDFs at once
- ✅ **Combined Output**: Merge multiple wordlists into single PDF
- ✅ **Professional Layout**: Clean typography for easy reading

## 🔐 BIP39 Use Cases

- **Seed Phrase References**: Print complete wordlists for offline verification
- **Recovery Guides**: Create backup reference materials
- **Educational Materials**: Teaching cryptocurrency security concepts
- **Language Learning**: Study BIP39 wordlists in different languages
- **Secure Storage**: Offline reference materials for air-gapped systems

## 🛠️ Advanced Options

### Command Line Options
```bash
python jinja_weasyprint_solution.py --help
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
abandon
ability
able
about
above
absent
absorb
abstract
absurd
abuse
access
accident
account
accuse
achieve
acid
```

*Note: This example shows the first 16 words from the BIP39 English wordlist. Each complete wordlist contains 32 words for a full page.*

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

## 🧰 Additional Tools

This repository includes optional utilities:

- **`generate_bip39_wordlists.py`**: Create wordlist files from official BIP39 data
- **`generate_wordlist_images.py`**: Generate AI images for words using Stable Diffusion
- **`wordlist_setup_script.py`**: Create sample data and test the generator

These tools can be used to prepare custom wordlists and visual mnemonics.

## 🔧 Integration

This tool can be integrated into larger workflows:
- **Cryptocurrency Wallets**: Generate reference materials for users
- **Security Training**: Create educational materials about seed phrases
- **Offline Storage**: Generate reference materials for air-gapped systems
- **Print Services**: Create professional reference materials

## 📄 License

Free to use and modify. Based on modern web technologies (Jinja2 + WeasyPrint) for professional PDF generation.
