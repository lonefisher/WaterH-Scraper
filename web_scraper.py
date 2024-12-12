import requests
from log_utils import setup_logger, log_execution
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

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

@log_execution(web_scraper_logger)
def extract_same_domain_links(html_content, base_url):
    """
    提取与主域名相同的链接
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    base_domain = urlparse(base_url).netloc
    links = set()
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        
        # 检查是否为相同域名
        if urlparse(full_url).netloc == base_domain:
            links.add(full_url)
    
    return links
