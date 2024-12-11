import requests
from log_utils import setup_logger, log_execution

# 设置日志记录器
web_scraper_logger = setup_logger('web_scraper', 'web_scraper.log')

@log_execution(web_scraper_logger)
def fetch_html_content(url):
    """
    Fetch the HTML content of a given URL.

    Parameters:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    try:
        # Send GET request with custom User-Agent
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        return response.text
    except requests.exceptions.RequestException as e:
        web_scraper_logger.error(f"Failed to fetch HTML content for URL: {url}. Error: {e}")
        raise
