#!/usr/bin/env python3
"""
Blog Article Converter
Converts markdown drafts to CSV format and updates blog.csv

Usage:
    python convert-to-csv.py [draft-file.md]
    python convert-to-csv.py --all  # Process all drafts
"""

import os
import sys
import csv
import yaml
import markdown
import re
from datetime import datetime
from pathlib import Path

# Configuration
DRAFTS_DIR = Path("../articles/drafts")
CSV_FILE = Path("../articles/blog.csv")
BACKUP_DIR = Path("../articles/backups")

class ArticleConverter:
    def __init__(self):
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
    def parse_markdown_file(self, file_path):
        """Parse a markdown file and extract frontmatter and content"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split frontmatter and content
        if content.startswith('---'):
            try:
                _, frontmatter, markdown_content = content.split('---', 2)
                metadata = yaml.safe_load(frontmatter.strip())
            except ValueError:
                raise ValueError(f"Invalid frontmatter format in {file_path}")
        else:
            raise ValueError(f"No frontmatter found in {file_path}")
            
        return metadata, markdown_content.strip()
    
    def markdown_to_html(self, markdown_content):
        """Convert markdown content to HTML"""
        # Configure markdown with extensions
        md = markdown.Markdown(extensions=[
            'tables',
            'fenced_code',
            'toc'
        ])
        
        html_content = md.convert(markdown_content)
        
        # Clean up and optimize HTML for CSV storage
        html_content = self.clean_html_for_csv(html_content)
        
        return html_content
    
    def clean_html_for_csv(self, html_content):
        """Clean and optimize HTML content for CSV storage"""
        # Replace multiple whitespace with single space
        html_content = re.sub(r'\s+', ' ', html_content)
        
        # Ensure proper escaping for CSV
        html_content = html_content.replace('"', '""')
        
        # Clean up common markdown artifacts
        html_content = html_content.strip()
        
        return html_content
    
    def format_date_for_csv(self, date_str):
        """Convert date string to ISO format required by CSV"""
        if isinstance(date_str, str):
            # Parse the date and convert to ISO format
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                return date_obj.strftime('%Y-%m-%dT00:00:00.000Z')
            except ValueError:
                # If already in ISO format, return as is
                return date_str
        return date_str
    
    def validate_metadata(self, metadata):
        """Validate required metadata fields"""
        required_fields = [
            'slug', 'title', 'date', 'shortDescription', 
            'metaDescription', 'authorName', 'reviewerName'
        ]
        
        missing_fields = [field for field in required_fields if field not in metadata]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Validate meta description length
        if len(metadata['metaDescription']) > 160:
            print(f"Warning: Meta description is {len(metadata['metaDescription'])} characters (recommended: 140-160)")
        
        # Validate slug format
        if not re.match(r'^[a-z0-9-]+$', metadata['slug']):
            raise ValueError(f"Invalid slug format: {metadata['slug']}. Use lowercase letters, numbers, and hyphens only.")
    
    def convert_article(self, markdown_file_path):
        """Convert a single markdown article to CSV format"""
        print(f"Processing: {markdown_file_path}")
        
        # Parse the markdown file
        metadata, markdown_content = self.parse_markdown_file(markdown_file_path)
        
        # Validate metadata
        self.validate_metadata(metadata)
        
        # Convert markdown to HTML
        html_content = self.markdown_to_html(markdown_content)
        
        # Format the CSV row
        csv_row = {
            'Slug': metadata['slug'],
            'Title': metadata['title'],
            'Date': self.format_date_for_csv(metadata['date']),
            'Cover': metadata.get('cover', 'https://via.placeholder.com/1200x800.png?text=Article+Cover'),
            'Short Description': metadata['shortDescription'],
            'Meta Description': metadata['metaDescription'],
            'Author Name': metadata['authorName'],
            'Reviewer Name': metadata['reviewerName'],
            'Content': html_content
        }
        
        return csv_row
    
    def backup_csv_file(self):
        """Create a backup of the existing CSV file"""
        if CSV_FILE.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = BACKUP_DIR / f"blog_backup_{timestamp}.csv"
            
            import shutil
            shutil.copy2(CSV_FILE, backup_file)
            print(f"Backup created: {backup_file.resolve()}")
    
    def update_csv_file(self, new_rows):
        """Update the CSV file with new or updated rows"""
        # Create backup
        self.backup_csv_file()
        
        # Read existing CSV data
        existing_rows = []
        existing_slugs = set()
        
        if CSV_FILE.exists():
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_rows.append(row)
                    existing_slugs.add(row['Slug'])
        
        # Update or add new rows
        updated_slugs = set()
        for new_row in new_rows:
            slug = new_row['Slug']
            
            if slug in existing_slugs:
                # Update existing row
                for i, row in enumerate(existing_rows):
                    if row['Slug'] == slug:
                        existing_rows[i] = new_row
                        print(f"Updated: {slug}")
                        break
            else:
                # Add new row
                existing_rows.append(new_row)
                print(f"Added: {slug}")
            
            updated_slugs.add(slug)
        
        # Write updated CSV file
        fieldnames = ['Slug', 'Title', 'Date', 'Cover', 'Short Description', 
                     'Meta Description', 'Author Name', 'Reviewer Name', 'Content']
        
        with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(existing_rows)
        
        print(f"CSV file updated: {CSV_FILE.resolve()}")
        return updated_slugs
    
    def process_all_drafts(self):
        """Process all markdown files in the drafts directory"""
        draft_files = list(DRAFTS_DIR.glob("*.md"))
        
        if not draft_files:
            print("No markdown files found in drafts directory")
            return
        
        # Filter out template file
        draft_files = [f for f in draft_files if f.name != 'article-template.md']
        
        converted_rows = []
        errors = []
        
        for draft_file in draft_files:
            try:
                csv_row = self.convert_article(draft_file)
                converted_rows.append(csv_row)
            except Exception as e:
                errors.append(f"{draft_file.name}: {str(e)}")
                print(f"Error processing {draft_file.name}: {e}")
        
        if converted_rows:
            updated_slugs = self.update_csv_file(converted_rows)
            print(f"\nSuccessfully processed {len(converted_rows)} articles")
            
            # Move processed files to processed folder
            processed_dir = DRAFTS_DIR / "processed"
            processed_dir.mkdir(exist_ok=True)
            
            for draft_file in draft_files:
                if any(row['Slug'] == draft_file.stem for row in converted_rows):
                    processed_file = processed_dir / draft_file.name
                    draft_file.rename(processed_file)
                    print(f"Moved to processed: {draft_file.name}")
        
        if errors:
            print(f"\nErrors encountered:")
            for error in errors:
                print(f"  - {error}")
    
    def process_single_file(self, file_path):
        """Process a single markdown file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"File not found: {file_path}")
            return
        
        try:
            csv_row = self.convert_article(file_path)
            self.update_csv_file([csv_row])
            print(f"Successfully processed: {file_path.name}")
            
            # Move to processed folder (always use the main drafts processed directory)
            processed_dir = DRAFTS_DIR / "processed"
            processed_dir.mkdir(exist_ok=True)
            processed_file = processed_dir / file_path.name
            
            # Only move if file is not already in processed directory
            if not str(file_path).endswith(f"processed/{file_path.name}"):
                file_path.rename(processed_file)
                print(f"Moved to processed: {file_path.name}")
            else:
                print(f"File already in processed directory: {file_path.name}")
            
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

def main():
    converter = ArticleConverter()
    
    if len(sys.argv) < 2:
        print("Usage: python convert-to-csv.py [draft-file.md] or --all")
        return
    
    if sys.argv[1] == '--all':
        converter.process_all_drafts()
    else:
        file_path = sys.argv[1]
        converter.process_single_file(file_path)

if __name__ == "__main__":
    main() 