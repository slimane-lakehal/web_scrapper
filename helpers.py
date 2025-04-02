import time
import random
from typing import Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from loguru import logger

def random_delay(min_delay: float = 1.0, max_delay: float = 3.0):
    """Add a random delay between requests to avoid rate limiting."""
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def clean_url(url: str) -> str:
    """Clean and normalize a URL."""
    parsed = urlparse(url)
    return urljoin(url, parsed.path)

def extract_links(soup: Any, base_url: str) -> list:
    """Extract and clean all links from a BeautifulSoup object."""
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith(('http://', 'https://')):
            links.append(href)
        else:
            links.append(urljoin(base_url, href))
    return list(set(links))  # Remove duplicates

def extract_text(soup: Any, selector: str) -> Optional[str]:
    """Extract text from an element using a CSS selector."""
    try:
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else None
    except Exception as e:
        logger.error(f"Error extracting text with selector {selector}: {str(e)}")
        return None

def extract_attributes(soup: Any, selector: str, attributes: list) -> Dict[str, Any]:
    """Extract multiple attributes from an element using a CSS selector."""
    try:
        element = soup.select_one(selector)
        if not element:
            return {}
        
        result = {}
        for attr in attributes:
            result[attr] = element.get(attr)
        return result
    except Exception as e:
        logger.error(f"Error extracting attributes with selector {selector}: {str(e)}")
        return {}

def validate_data(data: Dict[str, Any], required_fields: list) -> bool:
    """Validate that all required fields are present in the data."""
    return all(field in data for field in required_fields)

def sanitize_filename(filename: str) -> str:
    """Sanitize a filename to be safe for all operating systems."""
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()

def format_data(data: Dict[str, Any], format_type: str = 'json') -> str:
    """Format data into different output formats."""
    if format_type == 'json':
        import json
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif format_type == 'csv':
        import csv
        from io import StringIO
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
        return output.getvalue()
    else:
        raise ValueError(f"Unsupported format type: {format_type}") 