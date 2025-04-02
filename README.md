# Advanced Web Scraping Framework

A comprehensive web scraping framework that combines traditional scraping techniques with AI-powered extraction capabilities.

## Features

- **Base Scraper**: Core functionality for HTTP requests and data extraction
- **Dynamic Scraper**: Handles JavaScript-heavy websites using Selenium
- **AI Scraper**: Intelligent text extraction and processing using Jina
- **Utility Functions**: Common scraping helpers and data processing tools
- **Robust Error Handling**: Comprehensive error handling and retry logic
- **Rate Limiting**: Built-in rate limiting and random delays
- **Data Validation**: Input validation and data cleaning utilities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/web-scraper.git
cd web-scraper
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Scraping

```python
from scraper.base import BaseScraper, ScrapingConfig

# Configure the scraper
config = ScrapingConfig(
    base_url="https://example.com",
    timeout=30
)

# Create and run the scraper
scraper = BaseScraper(config)
data = scraper.run()
```

### Dynamic Content Scraping

```python
from scraper.dynamic import DynamicScraper

# Create a dynamic scraper
scraper = DynamicScraper(config, headless=True)

# Use context manager for automatic cleanup
with scraper:
    # Wait for specific elements
    element = scraper.wait_for_element(By.ID, "content")
    
    # Execute JavaScript
    result = scraper.execute_script("return document.title")
```

### AI-Powered Scraping

```python
from scraper.ai_scraper import AIScraper

# Create an AI scraper
scraper = AIScraper(config)

# Run the scraper
data = scraper.run()

# Save the results
scraper.save_data(data, "output.json")
```

## Project Structure

```
web_scraper/
├── scraper/
│   ├── __init__.py
│   ├── base.py
│   ├── dynamic.py
│   └── ai_scraper.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- BeautifulSoup4 for HTML parsing
- Selenium for dynamic content handling
- Jina for AI-powered text extraction
- All other contributors and maintainers 