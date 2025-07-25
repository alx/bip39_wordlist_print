#!/usr/bin/env python3
"""
Modern A4 Word Grid Generator using Jinja2 + WeasyPrint
Install: pip install jinja2 weasyprint pillow
"""

from jinja2 import Template
from weasyprint import HTML, CSS
import base64
from pathlib import Path
import os

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
    
    def generate_pdf(self, words, images_dir=None, output_file="word_grid.pdf"):
        """Generate PDF with word grid"""
        items = []
        
        # Ensure we have exactly 32 items
        words = words[:32] if len(words) > 32 else words + [f"Word{i+1}" for i in range(len(words), 32)]
        
        for i, word in enumerate(words):
            item = {"word": word, "image_data": None, "image_type": "png"}
            
            # Try to find matching image
            if images_dir:
                image_dir = Path(images_dir)
                possible_names = [
                    f"{word.lower()}.png", f"{word.lower()}.jpg", f"{word.lower()}.jpeg",
                    f"{i+1:02d}.png", f"{i+1:02d}.jpg", f"image{i+1}.png"
                ]
                
                for name in possible_names:
                    image_path = image_dir / name
                    if image_path.exists():
                        img_data, img_type = self.load_image_as_base64(image_path)
                        if img_data:
                            item["image_data"] = img_data
                            item["image_type"] = img_type
                        break
            
            items.append(item)
        
        # Render template
        html_content = self.template.render(title=self.title, items=items)
        
        # Generate PDF
        HTML(string=html_content).write_pdf(output_file)
        print(f"Generated: {output_file}")
        
        # Optionally save HTML for debugging
        with open(output_file.replace('.pdf', '.html'), 'w') as f:
            f.write(html_content)
        print(f"Debug HTML: {output_file.replace('.pdf', '.html')}")

# Example usage
if __name__ == "__main__":
    # Sample word list
    words = [
        "Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew",
        "Kiwi", "Lemon", "Mango", "Orange", "Papaya", "Quince", "Raspberry", "Strawberry",
        "Tangerine", "Ugli", "Vanilla", "Watermelon", "Xigua", "Yuzu", "Zucchini", "Avocado",
        "Blueberry", "Coconut", "Dragonfruit", "Eggplant", "Fennel", "Garlic", "Hazelnut", "Iceberg"
    ]
    
    # Create generator
    generator = WordGridGenerator("Fruit & Vegetable Reference")
    
    # Generate PDF (will use placeholder images if images_dir not found)
    generator.generate_pdf(words, images_dir="./images", output_file="modern_word_grid.pdf")
    
    # Alternative: Load from file
    # with open('wordlist.txt', 'r') as f:
    #     words = [line.strip() for line in f if line.strip()]
    # generator.generate_pdf(words, images_dir="./images")
