#!/usr/bin/env python3
"""
Modern A4 Word Grid Generator using Jinja2 + Google Chrome
Supports multiple wordlists with numbered image directories
Requires: pip install jinja2 pillow, and Google Chrome installed
"""

from jinja2 import Template
import base64
from pathlib import Path
import os
import argparse
import glob
import subprocess
import tempfile
import shutil

# HTML template with Mustache-like syntax
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @page {
            size: A4;
            margin: 1cm;
        }
        
        @media print {
            body {
                -webkit-print-color-adjust: exact;
                color-adjust: exact;
            }
        }
        
        body {
            font-family: 'Helvetica', sans-serif;
            margin: 0;
            padding: 0;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-template-rows: repeat(8, 1fr);
            gap: 6px;
            height: 27cm;
        }
        
        .cell {
            border: 0;
            display: flex;
            flex-direction: column;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            position: relative;
        }
        
        /* Corner cells with specific border radius */
        .cell:nth-child(1) {
            border-top-left-radius: 6px;
        }
        
        .cell:nth-child(4) {
            border-top-right-radius: 6px;
        }
        
        .cell:nth-child(29) {
            border-bottom-left-radius: 6px;
        }
        
        .cell:nth-child(32) {
            border-bottom-right-radius: 6px;
        }
        
        .index {
            position: absolute;
            top: -1px;
            left: 0;
            background: white;
            color: black;
            font-size: 14px;
            font-weight: normal;
            padding: 2px 4px;
        }
        
        .cell.no-image {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }

        .word {
            font-size: 14pt;
            text-align: right;
            color: white;
            text-transform: capitalize;
            line-height: 1.2;
            white-space: pre-line;
            padding: 5px 5px 0 0;
            position: relative;
            line-height: 2em;
  stroke: black;
  stroke-width: 4px;
paint-order: stroke fill;
-webkit-text-stroke: 5px black;
        }

        .word.no-image-text {
            color: #2c3e50;
            text-shadow: none;
        }
        
        .footer {
            position: fixed;
            bottom: -10px;
            display: flex;
            justify-content: center;
            font-family: 'Helvetica', sans-serif;
            font-size: 10pt;
            color: #666;
            height: 1cm;
            align-items: center;
            width: 100%;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="grid">
        {% for item in items %}
        {% if item.image_data %}
        <div class="cell" style="background-image: url('data:image/{{ item.image_type }};base64,{{ item.image_data }}');">
            <div class="index">{{ "%04d"|format(loop.index) }}</div>
            <div class="word">{{ item.word.replace(' ', '\n') }}</div>
        </div>
        {% else %}
        <div class="cell no-image">
            <div class="index">{{ "%04d"|format(loop.index) }}</div>
            <div class="word no-image-text">{{ item.word.replace(' ', '\n') }}</div>
        </div>
        {% endif %}
        {% endfor %}
    </div>
    
    <div class="footer">
        {{ current_page | default('001') }}/064
    </div>
</body>
</html>
"""

class WordGridGenerator:
    def __init__(self, title="Word Reference Grid"):
        self.template = Template(HTML_TEMPLATE)
        self.title = title
        
    def load_image_as_base64(self, image_path):
        """Convert image to base64 for embedding"""
        try:
            with open(image_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                ext = Path(image_path).suffix.lower().lstrip('.')
                if ext == 'jpg':
                    ext = 'jpeg'
                return img_data, ext
        except:
            return None, None
    
    def _generate_pdf_with_chrome(self, html_content, output_file):
        """Generate PDF using Google Chrome headless mode"""
        # Check if Chrome is available
        try:
            subprocess.run(['google-chrome', '--version'], 
                         check=True, capture_output=True, text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("Google Chrome not found. Please install Google Chrome.")
        
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', 
                                       delete=False, encoding='utf-8') as temp_html:
            temp_html.write(html_content)
            temp_html_path = temp_html.name
        
        try:
            # Convert HTML to PDF using Chrome
            cmd = [
                'google-chrome',
                '--headless',
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--no-pdf-header-footer',
                f'--print-to-pdf={output_file}',
                f'file://{temp_html_path}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to generate PDF with Chrome: {e.stderr}")
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_html_path)
            except OSError:
                pass
    
    def load_wordlist(self, wordlist_file):
        """Load words from a text file"""
        try:
            with open(wordlist_file, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
            return words
        except Exception as e:
            print(f"Error loading {wordlist_file}: {e}")
            return []
    
    def find_wordlists(self, wordlists_dir="wordlists"):
        """Find all wordlist files and their corresponding image directories"""
        wordlists_path = Path(wordlists_dir)
        if not wordlists_path.exists():
            print(f"Directory {wordlists_dir} not found!")
            return []
        
        wordlist_files = sorted(wordlists_path.glob("*.txt"))
        wordlist_data = []
        
        for txt_file in wordlist_files:
            # Get the base name (e.g., "001" from "001.txt")
            base_name = txt_file.stem
            
            # Find corresponding image directory
            img_dir = wordlists_path / base_name
            
            wordlist_info = {
                'name': base_name,
                'txt_file': txt_file,
                'img_dir': img_dir if img_dir.exists() else None,
                'words': self.load_wordlist(txt_file)
            }
            
            wordlist_data.append(wordlist_info)
            print(f"Found wordlist: {base_name} ({len(wordlist_info['words'])} words)")
            if wordlist_info['img_dir']:
                img_count = len(list(wordlist_info['img_dir'].glob("*.png")) + 
                              list(wordlist_info['img_dir'].glob("*.jpg")) + 
                              list(wordlist_info['img_dir'].glob("*.jpeg")))
                print(f"  → Images directory: {img_count} images")
            else:
                print(f"  → No images directory found")
        
        return wordlist_data
    
    def generate_pdf(self, words, images_dir=None, output_file="word_grid.pdf", wordlist_name=None):
        """Generate PDF with word grid for a single wordlist (supports multi-page)"""
        original_count = len(words)
        
        # Calculate number of pages needed (32 words per page)
        words_per_page = 32
        total_pages = max(1, (original_count + words_per_page - 1) // words_per_page)
        
        # Update title to include wordlist name
        title = f"{self.title}"
        if wordlist_name:
            title = f"{self.title} - {wordlist_name}"
        
        # Generate HTML pages
        all_html_pages = []
        
        for page_num in range(total_pages):
            # Get words for this page
            start_idx = page_num * words_per_page
            end_idx = min(start_idx + words_per_page, original_count)
            page_words = words[start_idx:end_idx]
            
            # Pad to 32 words if this is the last page and has fewer words
            if len(page_words) < words_per_page:
                page_words.extend([f"" for i in range(len(page_words), words_per_page)])
            
            # Build items for this page
            items = []
            for i, word in enumerate(page_words):
                word_index = start_idx + i + 1  # Global word index (1-based)
                item = {"word": word, "image_data": None, "image_type": "png"}
                
                # Try to find matching image by global word number
                if images_dir and word and word_index <= original_count:
                    image_dir = Path(images_dir)
                    # Try numbered format first (001.png, 002.png, etc.)
                    numbered_names = [
                        f"{word_index:03d}.png", f"{word_index:03d}.jpg", f"{word_index:03d}.jpeg",
                        f"{word_index:02d}.png", f"{word_index:02d}.jpg", f"{word_index:02d}.jpeg",
                        f"{word_index:01d}.png", f"{word_index:01d}.jpg", f"{word_index:01d}.jpeg"
                    ]
                    
                    # Also try word-based names as fallback
                    if word:
                        word_names = [
                            f"{word.lower()}.png", f"{word.lower()}.jpg", f"{word.lower()}.jpeg"
                        ]
                        all_names = numbered_names + word_names
                    else:
                        all_names = numbered_names
                    
                    for name in all_names:
                        image_path = image_dir / name
                        if image_path.exists():
                            img_data, img_type = self.load_image_as_base64(image_path)
                            if img_data:
                                item["image_data"] = img_data
                                item["image_type"] = img_type
                            break
                
                items.append(item)
            
            # Render template for this page
            current_page = f"{page_num + 1:03d}"
            total_pages_str = f"{total_pages:03d}"
            
            html_content = self.template.render(
                title=title, 
                items=items,
                current_page=current_page,
                total_pages=total_pages_str
            )
            all_html_pages.append(html_content)
        
        # Combine all pages into a single HTML document
        if len(all_html_pages) == 1:
            final_html = all_html_pages[0]
        else:
            # For multi-page, we need to combine them with page breaks
            combined_body_content = []
            for i, page_html in enumerate(all_html_pages):
                # Extract the body content from each page
                body_start = page_html.find('<body>') + 6
                body_end = page_html.find('</body>')
                body_content = page_html[body_start:body_end]
                
                if i > 0:
                    # Add page break before each page except the first
                    combined_body_content.append('<div style="page-break-before: always;"></div>')
                
                combined_body_content.append(body_content)
            
            # Use the first page as template and replace body content
            final_html = all_html_pages[0]
            body_start = final_html.find('<body>') + 6
            body_end = final_html.find('</body>')
            final_html = (final_html[:body_start] + 
                         '\n'.join(combined_body_content) + 
                         final_html[body_end:])
        
        # Generate PDF using Google Chrome
        self._generate_pdf_with_chrome(final_html, output_file)
        print(f"Generated: {output_file} ({total_pages} page{'s' if total_pages > 1 else ''})")
        
        # Optionally save HTML for debugging
        html_file = output_file.replace('.pdf', '.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Debug HTML: {html_file}")
    
    def generate_all_wordlists(self, wordlists_dir="wordlists", output_dir="output"):
        """Generate PDFs for all wordlists in the directory"""
        wordlist_data = self.find_wordlists(wordlists_dir)
        
        if not wordlist_data:
            print("No wordlists found!")
            return
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        for wordlist in wordlist_data:
            if not wordlist['words']:
                print(f"Skipping {wordlist['name']} - no words found")
                continue
            
            output_file = output_path / f"wordlist_{wordlist['name']}.pdf"
            
            print(f"\nProcessing wordlist: {wordlist['name']}")
            self.generate_pdf(
                words=wordlist['words'],
                images_dir=wordlist['img_dir'],
                output_file=str(output_file),
                wordlist_name=wordlist['name']
            )
        
        print(f"\n✅ All wordlists processed! Check the '{output_dir}' directory.")
    
    def generate_combined_pdf(self, wordlists_dir="wordlists", output_file="combined_wordlists.pdf"):
        """Generate a single PDF with all wordlists combined"""
        wordlist_data = self.find_wordlists(wordlists_dir)
        
        if not wordlist_data:
            print("No wordlists found!")
            return
        
        all_words = []
        all_images = []
        
        for wordlist in wordlist_data:
            words = wordlist['words'][:32]  # Limit each wordlist to 32 words
            img_dir = wordlist['img_dir']
            
            for i, word in enumerate(words):
                all_words.append(f"{word} ({wordlist['name']})")
                
                # Find corresponding image
                if img_dir:
                    numbered_names = [
                        f"{i+1:03d}.png", f"{i+1:03d}.jpg",
                        f"{i+1:02d}.png", f"{i+1:02d}.jpg",
                        f"{i+1:01d}.png", f"{i+1:01d}.jpg"
                    ]
                    
                    found_image = None
                    for name in numbered_names:
                        image_path = img_dir / name
                        if image_path.exists():
                            found_image = image_path
                            break
                    
                    all_images.append(found_image)
                else:
                    all_images.append(None)
        
        # Generate combined PDF
        print(f"\nGenerating combined PDF with {len(all_words)} words from {len(wordlist_data)} wordlists...")
        
        # For combined PDF, we need to handle images differently
        items = []
        for i, word in enumerate(all_words[:32]):  # Limit to 32 for single page
            item = {"word": word, "image_data": None, "image_type": "png"}
            
            if i < len(all_images) and all_images[i]:
                img_data, img_type = self.load_image_as_base64(all_images[i])
                if img_data:
                    item["image_data"] = img_data
                    item["image_type"] = img_type
            
            items.append(item)
        
        # Pad to 32 items if needed
        while len(items) < 32:
            items.append({"word": f"Empty{len(items)+1}", "image_data": None, "image_type": "png"})
        
        html_content = self.template.render(title="Combined Wordlists", items=items)
        self._generate_pdf_with_chrome(html_content, output_file)
        print(f"Generated combined PDF: {output_file}")

# CLI interface and example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate A4 word grids from wordlists with numbered images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all wordlists in wordlists/ directory
  python %(prog)s --all
  
  # Process specific wordlist
  python %(prog)s --wordlist wordlists/001.txt --images wordlists/001
  
  # Generate combined PDF from all wordlists
  python %(prog)s --combined
  
  # Custom title and output directory
  python %(prog)s --all --title "My Vocabulary" --output custom_output/

Directory structure expected:
  wordlists/
  ├── 001.txt          # First wordlist
  ├── 001/             # Images for first wordlist
  │   ├── 001.png      # Image for first word
  │   ├── 002.png      # Image for second word
  │   └── ...
  ├── 002.txt          # Second wordlist
  ├── 002/             # Images for second wordlist
  │   └── ...
  └── ...
        """)
    
    parser.add_argument("--wordlists-dir", default="wordlists", 
                       help="Directory containing wordlist files (default: wordlists)")
    parser.add_argument("--output", default="output", 
                       help="Output directory for generated PDFs (default: output)")
    parser.add_argument("--title", default="Word Reference Grid", 
                       help="Title for the word grids")
    
    # Mutually exclusive group for different modes
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--all", action="store_true", 
                           help="Process all wordlists in the directory")
    mode_group.add_argument("--combined", action="store_true", 
                           help="Generate single combined PDF from all wordlists")
    mode_group.add_argument("--wordlist", 
                           help="Process specific wordlist file")
    
    parser.add_argument("--images", 
                       help="Images directory (required when using --wordlist)")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.wordlist and not args.images:
        parser.error("--images is required when using --wordlist")
    
    # Create generator
    generator = WordGridGenerator(title=args.title)
    
    if args.all:
        # Process all wordlists
        print(f"🚀 Processing all wordlists in '{args.wordlists_dir}'...")
        generator.generate_all_wordlists(args.wordlists_dir, args.output)
        
    elif args.combined:
        # Generate combined PDF
        print(f"🚀 Generating combined PDF from all wordlists in '{args.wordlists_dir}'...")
        output_file = Path(args.output) / "combined_wordlists.pdf"
        Path(args.output).mkdir(exist_ok=True)
        generator.generate_combined_pdf(args.wordlists_dir, str(output_file))
        
    elif args.wordlist:
        # Process single wordlist
        print(f"🚀 Processing single wordlist: {args.wordlist}")
        
        # Load words
        words = generator.load_wordlist(args.wordlist)
        if not words:
            print("❌ No words found in wordlist!")
            exit(1)
        
        # Generate output filename
        wordlist_name = Path(args.wordlist).stem
        output_file = Path(args.output) / f"wordlist_{wordlist_name}.pdf"
        Path(args.output).mkdir(exist_ok=True)
        
        # Generate PDF
        generator.generate_pdf(
            words=words,
            images_dir=args.images,
            output_file=str(output_file),
            wordlist_name=wordlist_name
        )
    
    print("\n✅ Done! Check your output directory for generated PDFs.")
