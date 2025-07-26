#!/usr/bin/env python3
"""
BIP39 Wordlist Generator
Generates wordlist files from BIP39 wordlists using line-by-line mapping.
Each wordlist file contains words from the same line numbers across Chinese Simplified, English, and French BIP39 lists.
"""

import os
from pathlib import Path


def load_bip39_file(filepath):
    """Load words from a BIP39 file, returning list of words."""
    words = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # Remove any line numbers and whitespace
                word = line.strip()
                if word:
                    words.append(word)
        return words
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []


def generate_wordlists():
    """Generate wordlist files from BIP39 files using line-by-line mapping."""
    
    # Define file paths
    bip39_dir = Path("bip39")
    wordlists_dir = Path("wordlists")
    
    # BIP39 files to process
    bip39_files = {
        'chinese_simplified': bip39_dir / "chinese_simplified.txt",
        'english': bip39_dir / "english.txt", 
        'french': bip39_dir / "french.txt"
    }
    
    # Verify all BIP39 files exist
    for name, filepath in bip39_files.items():
        if not filepath.exists():
            print(f"Error: {filepath} not found!")
            return False
    
    # Load all BIP39 wordlists
    print("Loading BIP39 wordlists...")
    wordlists = {}
    for name, filepath in bip39_files.items():
        words = load_bip39_file(filepath)
        if not words:
            print(f"Error: Could not load words from {filepath}")
            return False
        wordlists[name] = words
        print(f"Loaded {len(words)} words from {name}")
    
    # Verify all wordlists have the same length
    word_counts = [len(words) for words in wordlists.values()]
    if len(set(word_counts)) != 1:
        print(f"Error: BIP39 files have different word counts: {word_counts}")
        return False
    
    total_words = word_counts[0]
    print(f"All files contain {total_words} words")
    
    # Create wordlists directory if it doesn't exist
    wordlists_dir.mkdir(exist_ok=True)
    
    # Generate wordlist files (32 lines at a time)
    chunk_size = 32
    num_files = total_words // chunk_size
    
    print(f"\nGenerating {num_files} wordlist files...")
    
    for file_num in range(num_files):
        # Calculate line range for this chunk
        start_line = file_num * chunk_size
        end_line = start_line + chunk_size
        
        # Create output filename with zero-padded number
        output_filename = f"{file_num + 1:03d}.txt"
        output_path = wordlists_dir / output_filename
        
        # Collect words for this chunk - one word per line from same line number across all three files
        chunk_words = []
        
        # For each line in the chunk, take one word from each language (same line number)
        for line_idx in range(start_line, end_line):
            if line_idx < len(wordlists['chinese_simplified']):
                # Add word from same line number in all three languages on same output line
                words_from_line = []
                words_from_line.append(wordlists['chinese_simplified'][line_idx])
                words_from_line.append(wordlists['english'][line_idx])
                words_from_line.append(wordlists['french'][line_idx])
                # Join the three words with spaces on a single line
                chunk_words.append(" ".join(words_from_line))
        
        # Write to wordlist file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for word_line in chunk_words:
                    f.write(f"{word_line}\n")
            
            print(f"Generated {output_filename}: {len(chunk_words)} lines (BIP39 lines {start_line+1}-{end_line})")
            
        except Exception as e:
            print(f"Error writing {output_path}: {e}")
            return False
    
    print(f"\nSuccessfully generated {num_files} wordlist files in {wordlists_dir}/")
    print(f"Each file contains words from the same line numbers across all three BIP39 lists")
    return True


def clear_existing_wordlists():
    """Clear existing wordlist files."""
    wordlists_dir = Path("wordlists")
    if not wordlists_dir.exists():
        return
    
    # Remove all .txt files in wordlists directory
    txt_files = list(wordlists_dir.glob("*.txt"))
    if txt_files:
        print(f"Clearing {len(txt_files)} existing wordlist files...")
        for txt_file in txt_files:
            try:
                txt_file.unlink()
                print(f"Removed {txt_file.name}")
            except Exception as e:
                print(f"Error removing {txt_file}: {e}")


def main():
    """Main function with command line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate wordlist files from BIP39 wordlists")
    parser.add_argument('--clear', action='store_true', help='Clear existing wordlist files before generating new ones')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be generated without creating files')
    
    args = parser.parse_args()
    
    print("BIP39 Wordlist Generator")
    print("=" * 50)
    
    if args.clear:
        clear_existing_wordlists()
        print()
    
    if args.dry_run:
        print("DRY RUN MODE - No files will be created")
        print()
    
    success = generate_wordlists()
    
    if success:
        print("\n✅ Wordlist generation completed successfully!")
        print("\nYou can now use the generated wordlists with:")
        print("  python jinja_chrome_solution.py --all")
    else:
        print("\n❌ Wordlist generation failed!")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())