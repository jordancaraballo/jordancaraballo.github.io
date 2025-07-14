import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding
import os
import re
from datetime import datetime

# Function to slugify titles for permalink
def slugify(value):
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[\s]+', '-', value)

# Load BibTeX file
def load_bibtex(file_path):
    with open(file_path, 'r', encoding='utf-8') as bibfile:
        parser = BibTexParser()
        parser.customization = homogenize_latex_encoding
        bib_database = bibtexparser.load(bibfile, parser=parser)
    return bib_database.entries

# Generate Markdown content
def create_markdown(entry, output_dir):
    title = entry.get('title', 'No Title').replace('{', '').replace('}', '')
    authors = entry.get('author', 'Unknown')
    year = entry.get('year', '1900')
    journal = entry.get('journal') or entry.get('booktitle') or 'Unknown Venue'
    url = entry.get('url') or ''
    excerpt = f"{title} by {authors.split('and')[0].strip()} et al."
    
    # Determine category
    if 'journal' in entry:
        category = 'journal'
    elif 'booktitle' in entry:
        category = 'conference'
    else:
        category = 'misc'

    # Create a slugified permalink
    slug = slugify(title)
    
    # Approximate date (January if not specified)
    date = f"{year}-01-01"

    # Citation formatting
    citation_authors = ', '.join([a.strip() for a in authors.split('and')])
    citation = f"{citation_authors} ({year}). \"{title}.\" <i>{journal}</i>."

    # Markdown content
    md_content = f"""---
title: "{title}"
collection: publications
category: {category}
permalink: /publication/{year}-{slug}
excerpt: "{excerpt}"
date: {date}
venue: "{journal}"
paperurl: "{url}"
citation: "{citation}"
---

This publication describes research work presented by {citation_authors}. See the venue for full details.
"""
    # Write to file
    filename = f"{year}-{slug}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as mdfile:
        mdfile.write(md_content)
    print(f"✅ Created: {filepath}")

# Main function
def main(bibtex_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    entries = load_bibtex(bibtex_path)
    for entry in entries:
        create_markdown(entry, output_dir)

# Usage Example
if __name__ == "__main__":
    # Path to your BibTeX file
    bibtex_file = "publications.bib"
    # Output directory for markdown files
    output_directory = "_publications"
    main(bibtex_file, output_directory)
