#!/usr/bin/env python3
"""
BIP39 Wordlist Image Generator using Stable Diffusion
Generates images for each line of wordlist files using webuiapi and AUTOMATIC1111's Stable Diffusion WebUI.
Each image represents the concepts from the multilingual words on that line.
"""

import os
import time
import argparse
from pathlib import Path
from typing import List, Tuple, Optional
import webuiapi
from tqdm import tqdm


class WordlistImageGenerator:
    """Generate images for BIP39 wordlist files using Stable Diffusion."""
    
    def __init__(self, 
                 host: str = "127.0.0.1", 
                 port: int = 7860,
                 prompt_template: str = None):
        """
        Initialize the image generator.
        
        Args:
            host: Stable Diffusion WebUI host
            port: Stable Diffusion WebUI port
            prompt_template: Custom prompt template for image generation
        """
        self.api = None
        self.host = host
        self.port = port
        
        # Default prompt template
        self.prompt_template = prompt_template or (
            "A symbolic illustration representing the concepts of '{words}', "
            "minimalist art style, clean lines, symbolic representation, "
            "digital art, concept art, highly detailed, 8k resolution"
        )
        
        # Default generation parameters
        self.generation_params = {
            "width": 1024,
            "height": 1024,
            "steps": 7,
            "cfg_scale": 2.0,
            "sampler_name": "DPM++ 2M SDE",
            "negative_prompt": (
                "ugly, blurry, low quality, distorted, deformed, "
                "text, watermark, signature, nsfw, explicit"
            )
        }
    
    def connect_api(self) -> bool:
        """
        Connect to Stable Diffusion WebUI API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            print(f"Connecting to Stable Diffusion WebUI at {self.host}:{self.port}...")
            self.api = webuiapi.WebUIApi(host=self.host, port=self.port)
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to Stable Diffusion WebUI: {e}")
            print("Make sure AUTOMATIC1111's WebUI is running with --api flag")
            return False
    
    def extract_words_from_line(self, line: str) -> List[str]:
        """
        Extract words from a wordlist line.
        
        Args:
            line: Line containing words (e.g., "的 abandon abaisser")
            
        Returns:
            List of words extracted from the line
        """
        words = line.strip().split()
        # Filter out empty strings and return unique words
        unique_words = []
        for word in words:
            if word and word not in unique_words:
                unique_words.append(word)
        return unique_words
    
    def create_prompt(self, words: List[str]) -> str:
        """
        Create a Stable Diffusion prompt from words.
        
        Args:
            words: List of words to incorporate into prompt
            
        Returns:
            Formatted prompt string
        """
        # Join words with commas for better prompt structure
        words_str = ", ".join(words)
        return self.prompt_template.format(words=words_str)
    
    def generate_image(self, prompt: str, seed: Optional[int] = None) -> Optional[any]:
        """
        Generate an image using Stable Diffusion.
        
        Args:
            prompt: Text prompt for image generation
            seed: Optional seed for reproducible results
            
        Returns:
            Generated image object or None if failed
        """
        if not self.api:
            print("❌ API not connected!")
            return None
        
        try:
            params = self.generation_params.copy()
            params["prompt"] = prompt
            if seed is not None:
                params["seed"] = seed
            
            result = self.api.txt2img(**params)
            return result.image
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return None
    
    def save_image(self, image: any, filepath: Path) -> bool:
        """
        Save generated image to file.
        
        Args:
            image: PIL Image object
            filepath: Path where to save the image
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Save image
            image.save(filepath, "PNG")
            return True
            
        except Exception as e:
            print(f"❌ Error saving image to {filepath}: {e}")
            return False
    
    def process_wordlist_file(self, 
                             wordlist_path: Path, 
                             dry_run: bool = False,
                             force_regenerate: bool = False) -> Tuple[int, int]:
        """
        Process a single wordlist file and generate images.
        
        Args:
            wordlist_path: Path to the wordlist file
            dry_run: If True, only show what would be done
            force_regenerate: If True, regenerate existing images
            
        Returns:
            Tuple of (successful_generations, total_lines)
        """
        # Determine output directory
        wordlist_name = wordlist_path.stem  # e.g., "001" from "001.txt"
        output_dir = wordlist_path.parent / wordlist_name
        
        # Read wordlist file
        try:
            with open(wordlist_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ Error reading {wordlist_path}: {e}")
            return 0, 0
        
        print(f"\n📁 Processing {wordlist_path.name} ({len(lines)} lines)")
        if dry_run:
            print("🔍 DRY RUN MODE - No images will be generated")
        
        successful = 0
        
        for line_idx, line in enumerate(lines, 1):
            # Create output filename (001.png, 002.png, etc.)
            image_filename = f"{line_idx:03d}.png"
            image_path = output_dir / image_filename
            
            # Skip if image already exists and not forcing regeneration
            if image_path.exists() and not force_regenerate:
                print(f"⏭️  Skipping {image_filename} (already exists)")
                successful += 1
                continue
            
            # Extract words and create prompt
            words = self.extract_words_from_line(line)
            if not words:
                print(f"⚠️  Skipping line {line_idx} - no words found")
                continue
            
            prompt = self.create_prompt(words)
            
            if dry_run:
                print(f"🔍 Line {line_idx}: {line}")
                print(f"   Words: {words}")
                print(f"   Prompt: {prompt}")
                print(f"   Would save to: {image_path}")
                successful += 1
                continue
            
            # Generate and save image
            print(f"🎨 Generating {image_filename}: {' '.join(words)}")
            
            # Use line index as seed for reproducible results
            seed = hash(f"{wordlist_name}_{line_idx}") % (2**32)
            image = self.generate_image(prompt, seed=seed)
            
            if image and self.save_image(image, image_path):
                print(f"✅ Saved {image_filename}")
                successful += 1
            else:
                print(f"❌ Failed to generate/save {image_filename}")
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.5)
        
        return successful, len(lines)
    
    def process_all_wordlists(self, 
                             wordlists_dir: str = "wordlists",
                             dry_run: bool = False,
                             force_regenerate: bool = False,
                             file_pattern: str = "*.txt") -> None:
        """
        Process all wordlist files in the directory.
        
        Args:
            wordlists_dir: Directory containing wordlist files
            dry_run: If True, only show what would be done
            force_regenerate: If True, regenerate existing images
            file_pattern: Pattern to match wordlist files
        """
        wordlists_path = Path(wordlists_dir)
        if not wordlists_path.exists():
            print(f"❌ Directory {wordlists_dir} not found!")
            return
        
        # Find all wordlist files
        wordlist_files = sorted(wordlists_path.glob(file_pattern))
        if not wordlist_files:
            print(f"❌ No wordlist files found in {wordlists_dir}!")
            return
        
        print(f"🚀 Found {len(wordlist_files)} wordlist files")
        
        total_successful = 0
        total_lines = 0
        
        # Process each wordlist file
        for wordlist_file in tqdm(wordlist_files, desc="Processing wordlists"):
            successful, lines = self.process_wordlist_file(
                wordlist_file, 
                dry_run=dry_run,
                force_regenerate=force_regenerate
            )
            total_successful += successful
            total_lines += lines
        
        # Summary
        print(f"\n📊 Summary:")
        print(f"   Total wordlist files: {len(wordlist_files)}")
        print(f"   Total lines processed: {total_lines}")
        print(f"   Successful generations: {total_successful}")
        
        if not dry_run:
            print(f"   Success rate: {total_successful/total_lines*100:.1f}%")


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Generate images for BIP39 wordlist files using Stable Diffusion"
    )
    
    parser.add_argument(
        '--wordlists-dir', 
        default='wordlists',
        help='Directory containing wordlist files (default: wordlists)'
    )
    
    parser.add_argument(
        '--host', 
        default='127.0.0.1',
        help='Stable Diffusion WebUI host (default: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=7860,
        help='Stable Diffusion WebUI port (default: 7860)'
    )
    
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Show what would be done without generating images'
    )
    
    parser.add_argument(
        '--force', 
        action='store_true',
        help='Regenerate existing images'
    )
    
    parser.add_argument(
        '--prompt-template',
        help='Custom prompt template (use {words} placeholder)'
    )
    
    parser.add_argument(
        '--file-pattern',
        default='*.txt',
        help='Pattern to match wordlist files (default: *.txt)'
    )
    
    args = parser.parse_args()
    
    print("🎨 BIP39 Wordlist Image Generator")
    print("=" * 50)
    
    # Create generator
    generator = WordlistImageGenerator(
        host=args.host,
        port=args.port,
        prompt_template=args.prompt_template
    )
    
    # Connect to API (skip in dry-run mode)
    if not args.dry_run:
        if not generator.connect_api():
            print("\n💡 Tip: Start AUTOMATIC1111's WebUI with: python launch.py --api")
            return 1
    
    # Process wordlists
    generator.process_all_wordlists(
        wordlists_dir=args.wordlists_dir,
        dry_run=args.dry_run,
        force_regenerate=args.force,
        file_pattern=args.file_pattern
    )
    
    if not args.dry_run:
        print("\n✅ Image generation completed!")
        print("You can now use the generated images with:")
        print("  python jinja_chrome_solution.py --all")
    
    return 0


if __name__ == "__main__":
    exit(main())
