from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru import logger
from .base import BaseScraper, ScrapingConfig

class DynamicScraper(BaseScraper):
    """Scraper for JavaScript-heavy websites using Selenium."""
    
    def __init__(self, config: ScrapingConfig, headless: bool = True):
        super().__init__(config)
        self.headless = headless
        self.driver = None
        self.wait = None
        self._setup_driver()
    
    def _setup_driver(self):
        """Configure and initialize the Selenium WebDriver."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={self.ua.random}')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, self.config.timeout)
    
    def get_page(self, url: str) -> Any:
        """Load and wait for dynamic content to be ready."""
        try:
            self.driver.get(url)
            # Wait for the body to be present
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            return self.driver
        except TimeoutException as e:
            logger.error(f"Timeout while loading {url}: {str(e)}")
            raise
    
    def wait_for_element(self, by: By, value: str, timeout: Optional[int] = None):
        """Wait for a specific element to be present and visible."""
        timeout = timeout or self.config.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException as e:
            logger.error(f"Timeout waiting for element {value}: {str(e)}")
            raise
    
    def execute_script(self, script: str) -> Any:
        """Execute JavaScript code in the browser context."""
        try:
            return self.driver.execute_script(script)
        except Exception as e:
            logger.error(f"Error executing script: {str(e)}")
            raise
    
    def close(self):
        """Clean up resources."""
        if self.driver:
            self.driver.quit()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 