from typing import Optional, Dict, Any
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from pydantic import BaseModel, HttpUrl

class ScrapingConfig(BaseModel):
    """Configuration for scraping operations."""
    base_url: HttpUrl
    headers: Optional[Dict[str, str]] = None
    timeout: int = 30
    max_retries: int = 3
    delay: float = 1.0

class BaseScraper:
    """Base class for all scrapers with common functionality."""
    
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.session = requests.Session()
        self.ua = UserAgent()
        self._setup_session()
        
    def _setup_session(self):
        """Configure the session with default headers and settings."""
        default_headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        if self.config.headers:
            default_headers.update(self.config.headers)
        self.session.headers.update(default_headers)
    
    @retry(
        stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def get_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a webpage with retry logic."""
        try:
            response = self.session.get(
                url,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise
    
    def extract_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract data from BeautifulSoup object. To be implemented by subclasses."""
        raise NotImplementedError
    
    def process_data(self, data: Dict[str, Any]) -> Any:
        """Process extracted data. To be implemented by subclasses."""
        raise NotImplementedError
    
    def save_data(self, data: Any, filename: str):
        """Save processed data. To be implemented by subclasses."""
        raise NotImplementedError
    
    def run(self):
        """Execute the complete scraping workflow."""
        try:
            soup = self.get_page(str(self.config.base_url))
            raw_data = self.extract_data(soup)
            processed_data = self.process_data(raw_data)
            return processed_data
        except Exception as e:
            logger.error(f"Error in scraping workflow: {str(e)}")
            raise 