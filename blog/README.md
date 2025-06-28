# Blog Article System - Complete Guide

This document explains how to use the blog article system that outputs to CSV format for marketing automation.

## 📋 System Overview

The system uses a **two-step process**:

1. **Draft Creation**: Write articles in markdown with structured metadata
2. **CSV Conversion**: Automated script converts drafts to CSV format

### Directory Structure

```
blog/
├── articles/
│   ├── blog.csv                    # Main CSV file with all articles
│   ├── drafts/                     # Markdown drafts directory
│   │   ├── article-template.md     # Template for new articles
│   │   ├── processed/              # Completed drafts (auto-created)
│   │   └── [new-article].md        # Your draft files
│   └── backups/                    # CSV backups (auto-created)
├── scripts/
│   ├── convert-to-csv.py          # Conversion script
│   └── requirements.txt           # Python dependencies
├── ai-content-writer-prompt.md    # AI writer instructions
└── README.md                      # This file
```

## 🚀 Quick Start Guide

### 1. Setup (One-time)

Install Python dependencies:

```bash
cd blog/scripts
pip install -r requirements.txt
```

### 2. Create New Article

1. **Copy the template**:

   ```bash
   cp blog/articles/drafts/article-template.md blog/articles/drafts/my-new-article.md
   ```

2. **Edit the frontmatter** with your article metadata:

   ```yaml
   ---
   slug: my-new-article
   title: "My New Article Title with Primary Keyword"
   date: 2025-06-15
   cover: https://example.com/cover-image.png
   shortDescription: "Brief engaging summary..."
   metaDescription: "SEO meta description under 160 chars..."
   authorName: artem-vysotsky
   reviewerName: sergey-vysotsky
   primaryKeyword: main keyword
   secondaryKeywords: ["keyword1", "keyword2"]
   contentFormat: "Best Of"
   ---
   ```

3. **Write your content** in markdown below the frontmatter

### 3. Convert to CSV

**Process single article**:

```bash
cd blog/scripts
python convert-to-csv.py ../articles/drafts/my-new-article.md
```

**Process all drafts**:

```bash
cd blog/scripts
python convert-to-csv.py --all
```

The script will:

- ✅ Validate your metadata
- ✅ Convert markdown to HTML
- ✅ Update the CSV file
- ✅ Create backups
- ✅ Move processed files to `processed/` folder

## 📝 Writing Guidelines

### Required Frontmatter Fields

| Field              | Description              | Example                         |
| ------------------ | ------------------------ | ------------------------------- |
| `slug`             | URL-friendly identifier  | `best-ai-tools-2025`            |
| `title`            | SEO-optimized title      | `"Best AI Tools in 2025"`       |
| `date`             | Publication date         | `2025-06-15`                    |
| `cover`            | Cover image URL          | `https://example.com/image.png` |
| `shortDescription` | 2-3 sentence summary     | `"Learn about..."`              |
| `metaDescription`  | SEO meta (140-160 chars) | `"Discover the best..."`        |
| `authorName`       | Hyphenated author name   | `artem-vysotsky`                |
| `reviewerName`     | Hyphenated reviewer name | `sergey-vysotsky`               |

### Content Format Options

Choose your content format:

- **"Best Of"**: Comprehensive comparison articles
- **"Alternative"**: Competitor alternative articles
- **"Guide"**: How-to and tutorial content
- **"Comparison"**: Direct product comparisons

### Writing Best Practices

1. **Authority Introduction**:

   ```markdown
   Hello, I'm [Author] and I've been working with [field] for [X years].
   In my experience [specific area], I've discovered that [problem statement].
   ```

2. **Technical Credibility**:

   - Use specific model names: "GPT-4o", "Claude 3.7"
   - Include version updates: "February 2025 update"
   - Add pricing details: "$9.99/month", "3,000 points per day"

3. **SEO Optimization**:
   - Primary keyword in: title, meta description, first paragraph, one H2
   - Use H2 for main sections, H3 for subsections
   - Include internal links to related articles

## 🛠️ Advanced Usage

### Batch Processing

Process multiple drafts at once:

```bash
# Process all .md files in drafts folder
python convert-to-csv.py --all
```

### Validation Checks

The script automatically validates:

- ✅ Required metadata fields
- ✅ Slug format (lowercase, hyphens only)
- ✅ Meta description length (warns if >160 chars)
- ✅ Date format conversion
- ✅ HTML escaping for CSV

### Backup System

Every CSV update creates a timestamped backup:

```
blog/articles/backups/blog_backup_20250615_143022.csv
```

### Error Handling

Common errors and solutions:

| Error                     | Solution                                     |
| ------------------------- | -------------------------------------------- |
| `No frontmatter found`    | Add `---` before and after metadata          |
| `Missing required fields` | Check all required frontmatter fields        |
| `Invalid slug format`     | Use lowercase letters, numbers, hyphens only |
| `File not found`          | Check file path and spelling                 |

## 📊 CSV Structure

The final CSV contains these columns:

| Column              | Source                       | Description         |
| ------------------- | ---------------------------- | ------------------- |
| `Slug`              | frontmatter.slug             | URL identifier      |
| `Title`             | frontmatter.title            | Article title       |
| `Date`              | frontmatter.date             | ISO format date     |
| `Cover`             | frontmatter.cover            | Cover image URL     |
| `Short Description` | frontmatter.shortDescription | Brief summary       |
| `Meta Description`  | frontmatter.metaDescription  | SEO meta            |
| `Author Name`       | frontmatter.authorName       | Author identifier   |
| `Reviewer Name`     | frontmatter.reviewerName     | Reviewer identifier |
| `Content`           | markdown content             | Full HTML content   |

## 🔄 Workflow Examples

### Example 1: New "Best Of" Article

1. **Create draft**:

   ```bash
   cp article-template.md best-ai-chatbots-2025.md
   ```

2. **Edit frontmatter**:

   ```yaml
   slug: best-ai-chatbots-2025
   title: "Best AI Chatbots in 2025 – Compare 8 Top Platforms"
   contentFormat: "Best Of"
   primaryKeyword: best AI chatbots
   ```

3. **Write content** following "Best Of" pattern
4. **Convert**: `python convert-to-csv.py best-ai-chatbots-2025.md`

### Example 2: Competitor Alternative Article

1. **Create draft** with "Alternative" format:

   ```yaml
   slug: best-chatgpt-alternative-2025
   title: "The Best ChatGPT Alternative in 2025"
   contentFormat: "Alternative"
   primaryKeyword: ChatGPT alternative
   ```

2. **Write content** following "Alternative" pattern
3. **Convert** to CSV

### Example 3: Bulk Processing

1. **Create multiple drafts** in `drafts/` folder
2. **Process all at once**:
   ```bash
   python convert-to-csv.py --all
   ```
3. **Review results** and check `processed/` folder

## 🎯 Quality Checklist

Before converting to CSV, verify:

### Content Quality

- [ ] 1500-3000 word count
- [ ] Personal authority established
- [ ] Technical details included
- [ ] Use cases and examples provided
- [ ] Balanced perspective maintained

### SEO Optimization

- [ ] Primary keyword in title, meta, first paragraph, H2
- [ ] Meta description 140-160 characters
- [ ] Proper header hierarchy (H2 → H3 → H4)
- [ ] Internal links to related content
- [ ] Alt text for images (max 4 words)

### CSV Compatibility

- [ ] All required frontmatter fields completed
- [ ] Slug uses lowercase and hyphens only
- [ ] Date in YYYY-MM-DD format
- [ ] Author/reviewer names hyphenated
- [ ] Content follows markdown standards

## 🚨 Troubleshooting

### Common Issues

**Script won't run**:

```bash
# Install dependencies
pip install -r requirements.txt

# Check Python version (requires 3.6+)
python --version
```

**Invalid frontmatter**:

- Ensure `---` before and after metadata
- Check YAML syntax (proper indentation, quotes)
- Verify all required fields present

**CSV formatting errors**:

- Check for unescaped quotes in content
- Verify slug format (no spaces, uppercase)
- Ensure date format is YYYY-MM-DD

**Permission errors**:

```bash
# Make script executable
chmod +x convert-to-csv.py

# Check file permissions
ls -la blog/articles/
```

### Getting Help

1. **Check error messages** - they usually indicate the specific issue
2. **Validate frontmatter** using online YAML validators
3. **Test with template** - copy `article-template.md` and modify
4. **Review examples** in existing CSV entries

## 📈 Tips for Success

1. **Start with template**: Always copy from `article-template.md`
2. **Validate early**: Check frontmatter before writing content
3. **Use proven patterns**: Follow "Best Of" or "Alternative" formats
4. **Test frequently**: Convert single articles before batch processing
5. **Backup regularly**: Script creates backups, but manual backups are good too

This workflow ensures consistent, high-quality articles that integrate seamlessly with your marketing automation system.
