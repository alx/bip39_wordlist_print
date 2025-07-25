#!/usr/bin/env python3
"""
Modern A4 Word Grid Generator using Jinja2 + WeasyPrint
Supports multiple wordlists with numbered image directories
Install: pip install jinja2 weasyprint pillow
"""

from jinja2 import Template
from weasyprint import HTML, CSS
import base64
from pathlib import Path
import os
import argparse
import glob

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
        
        body {
            font-family: 'Helvetica', sans-serif;
            margin: 0;
            padding: 0;
        }
        
        .header {
            text-align: center;
            font-size: 18pt;
            font-weight: bold;
            margin-bottom: 1cm;
            color: #333;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-template-rows: repeat(8, 1fr);
            gap: 0.5cm;
            height: 20cm;
        }
        
        .cell {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 0.3cm;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .cell img {
            max-width: 80%;
            max-height: 60%;
            object-fit: contain;
            border-radius: 4px;
            margin-bottom: 0.2cm;
        }
        
        .word {
            font-size: 10pt;
            font-weight: bold;
            text-align: center;
            color: #2c3e50;
            text-transform: capitalize;
        }
        
        .placeholder-img {
            width: 2cm;
            height: 1.5cm;
            background: linear-gradient(45deg, #74b9ff, #0984e3);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 8pt;
            margin-bottom: 0.2cm;
        }
    </style>
</head>
<body>
    <div class="header">{{ title }}</div>
    
    <div class="grid">
        {% for item in items %}
        <div class="cell">
            {% if item.image_data %}
            <img src="data:image/{{ item.image_type }};base64,{{ item.image_data }}" alt="{{ item.word }}">
            {% else %}
            <div class="placeholder-img">IMG</div>
            {% endif %}
            <div class="word">{{ item.word }}</div>
        </div>
        {% endfor %}
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
        """Generate PDF with word grid for a single wordlist"""
        items = []
        
        # Ensure we have exactly 32 items
        original_count = len(words)
        words = words[:32] if len(words) > 32 else words + [f"Word{i+1}" for i in range(len(words), 32)]
        
        for i, word in enumerate(words):
            item = {"word": word, "image_data": None, "image_type": "png"}
            
            # Try to find matching image by number (001.png, 002.png, etc.)
            if images_dir and i < original_count:  # Only look for images for actual words
                image_dir = Path(images_dir)
                # Try numbered format first (001.png, 002.png, etc.)
                numbered_names = [
                    f"{i+1:03d}.png", f"{i+1:03d}.jpg", f"{i+1:03d}.jpeg",
                    f"{i+1:02d}.png", f"{i+1:02d}.jpg", f"{i+1:02d}.jpeg",
                    f"{i+1:01d}.png", f"{i+1:01d}.jpg", f"{i+1:01d}.jpeg"
                ]
                
                # Also try word-based names as fallback
                word_names = [
                    f"{word.lower()}.png", f"{word.lower()}.jpg", f"{word.lower()}.jpeg"
                ]
                
                all_names = numbered_names + word_names
                
                for name in all_names:
                    image_path = image_dir / name
                    if image_path.exists():
                        img_data, img_type = self.load_image_as_base64(image_path)
                        if img_data:
                            item["image_data"] = img_data
                            item["image_type"] = img_type
                        break
            
            items.append(item)
        
        # Update title to include wordlist name
        title = f"{self.title}"
        if wordlist_name:
            title = f"{self.title} - {wordlist_name}"
        
        # Render template
        html_content = self.template.render(title=title, items=items)
        
        # Generate PDF
        HTML(string=html_content).write_pdf(output_file)
        print(f"Generated: {output_file}")
        
        # Optionally save HTML for debugging
        html_file = output_file.replace('.pdf', '.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
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
        HTML(string=html_content).write_pdf(output_file)
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