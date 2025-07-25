#!/usr/bin/env python3
"""
Setup script to create sample wordlist directory structure
and test the word grid generator
"""

import os
from pathlib import Path
import argparse
import random

def create_sample_wordlists():
    """Create sample wordlist directory structure"""
    
    # Sample word categories
    wordlist_data = {
        "001": [  # Fruits
            "Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew",
            "Kiwi", "Lemon", "Mango", "Orange", "Papaya", "Quince", "Raspberry", "Strawberry",
            "Tangerine", "Ugli", "Vanilla", "Watermelon", "Xigua", "Yuzu", "Zucchini", "Avocado",
            "Blueberry", "Coconut", "Dragonfruit", "Eggplant", "Fennel", "Garlic", "Hazelnut", "Iceberg"
        ],
        "002": [  # Animals
            "Ant", "Bear", "Cat", "Dog", "Elephant", "Fox", "Giraffe", "Horse",
            "Iguana", "Jaguar", "Kangaroo", "Lion", "Mouse", "Newt", "Owl", "Penguin",
            "Quail", "Rabbit", "Snake", "Tiger", "Unicorn", "Vulture", "Wolf", "Xenops",
            "Yak", "Zebra", "Aardvark", "Badger", "Cheetah", "Dolphin", "Eagle", "Flamingo"
        ],
        "003": [  # Colors
            "Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Pink", "Brown",
            "Black", "White", "Gray", "Violet", "Indigo", "Turquoise", "Magenta", "Cyan",
            "Maroon", "Navy", "Olive", "Lime", "Aqua", "Teal", "Silver", "Gold",
            "Crimson", "Scarlet", "Azure", "Beige", "Coral", "Ivory", "Khaki", "Lavender"
        ]
    }
    
    # Create main directory
    wordlists_dir = Path("wordlists")
    wordlists_dir.mkdir(exist_ok=True)
    
    print("📁 Creating sample wordlist structure...")
    
    for list_id, words in wordlist_data.items():
        # Create text file
        txt_file = wordlists_dir / f"{list_id}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            for word in words:
                f.write(f"{word}\n")
        
        print(f"   Created: {txt_file} ({len(words)} words)")
        
        # Create image directory
        img_dir = wordlists_dir / list_id
        img_dir.mkdir(exist_ok=True)
        
        # Create placeholder images if imagemagick is available
        try:
            import subprocess
            # Check if ImageMagick convert is available
            result = subprocess.run(['convert', '-version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                create_placeholder_images(img_dir, words, list_id)
            else:
                print(f"   📷 ImageMagick not found - skipping image creation for {list_id}")
        except FileNotFoundError:
            print(f"   📷 ImageMagick not found - skipping image creation for {list_id}")
    
    print(f"\n✅ Sample wordlist structure created in '{wordlists_dir}'!")
    return wordlists_dir

def create_placeholder_images(img_dir, words, list_id):
    """Create placeholder images using ImageMagick"""
    import subprocess
    
    # Color schemes for different wordlists
    color_schemes = {
        "001": ("#FF6B6B", "#4ECDC4"),  # Fruits - red/teal
        "002": ("#45B7D1", "#96CEB4"),  # Animals - blue/green  
        "003": ("#FECA57", "#FF9FF3"),  # Colors - yellow/pink
    }
    
    bg_color, text_color = color_schemes.get(list_id, ("#74b9ff", "#0984e3"))
    
    print(f"   📷 Creating placeholder images for {list_id}...")
    
    for i, word in enumerate(words, 1):
        img_file = img_dir / f"{i:03d}.png"
        
        # Create placeholder image with ImageMagick
        cmd = [
            'convert',
            '-size', '300x200',
            '-background', bg_color,
            '-fill', text_color,
            '-gravity', 'center',
            '-pointsize', '24',
            '-font', 'Arial-Bold',
            f'label:{word}',
            str(img_file)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            # Fallback to simpler command
            simple_cmd = [
                'convert',
                '-size', '300x200',
                '-background', bg_color,
                '-fill', text_color,
                '-gravity', 'center',
                f'label:{word}',
                str(img_file)
            ]
            try:
                subprocess.run(simple_cmd, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"      ❌ Failed to create {img_file}: {e}")
                continue
    
    print(f"      ✅ Created {len(words)} placeholder images")

def test_generator():
    """Test the word grid generator with sample data"""
    try:
        from jinja_weasyprint_solution import WordGridGenerator
    except ImportError:
        print("❌ Cannot import WordGridGenerator. Make sure the main script is available.")
        return False
    
    print("\n🧪 Testing word grid generator...")
    
    # Test with sample wordlists
    generator = WordGridGenerator("Test Word Grids")
    
    try:
        # Test processing all wordlists
        generator.generate_all_wordlists("wordlists", "test_output")
        print("✅ All wordlists processed successfully!")
        
        # Test combined PDF
        generator.generate_combined_pdf("wordlists", "test_output/combined_test.pdf")
        print("✅ Combined PDF generated successfully!")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def show_usage_examples():
    """Show usage examples for the word grid generator"""
    print("""
🚀 Word Grid Generator Usage Examples:

1. Process all wordlists:
   python word_grid_generator.py --all

2. Process specific wordlist:
   python word_grid_generator.py --wordlist wordlists/001.txt --images wordlists/001

3. Generate combined PDF:
   python word_grid_generator.py --combined

4. Custom output directory and title:
   python word_grid_generator.py --all --output my_grids --title "My Vocabulary Cards"

5. Process all with custom settings:
   python word_grid_generator.py --all \\
     --wordlists-dir my_wordlists \\
     --output final_pdfs \\
     --title "Language Learning Cards"

📁 Directory Structure:
   wordlists/
   ├── 001.txt              # Wordlist file
   ├── 001/                 # Image directory
   │   ├── 001.png         # First word image
   │   ├── 002.png         # Second word image
   │   └── ...
   ├── 002.txt
   ├── 002/
   └── ...

🖼️  Image Naming:
   - Images should be numbered: 001.png, 002.png, etc.
   - Supported formats: PNG, JPG, JPEG
   - Images are matched to words by position in the wordlist
    """)

def main():
    parser = argparse.ArgumentParser(
        description="Setup and test wordlist directory structure"
    )
    
    parser.add_argument("--create-samples", action="store_true",
                       help="Create sample wordlist directory structure")
    parser.add_argument("--test", action="store_true",
                       help="Test the word grid generator")
    parser.add_argument("--usage", action="store_true",
                       help="Show usage examples")
    parser.add_argument("--all", action="store_true",
                       help="Create samples, test, and show usage")
    
    args = parser.parse_args()
    
    if args.all or not any(vars(args).values()):
        # Default action: do everything
        create_sample_wordlists()
        test_generator()
        show_usage_examples()
    else:
        if args.create_samples:
            create_sample_wordlists()
        
        if args.test:
            test_generator()
        
        if args.usage:
            show_usage_examples()

if __name__ == "__main__":
    main()