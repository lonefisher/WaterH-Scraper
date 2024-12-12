import requests
from log_utils import setup_logger, log_execution
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from config import MAX_CHILD_PAGES

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
    提取与主域名相同的有效链接，只排除媒体和系统文件
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    base_domain = urlparse(base_url).netloc
    links = set()
    
    # 只保留最基本的排除路径
    excluded_paths = {
        '/wp-content/',  # WordPress 媒体文件
        '/assets/',      # 静态资源
        '/images/',      # 图片目录
        '/downloads/'    # 下载文件
    }
    
    # 基本的文件扩展名排除
    excluded_extensions = {
        # 图片
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp',
        # 文档
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        # 媒体
        '.mp3', '.mp4', '.wav', '.avi', '.mov',
        # 压缩包
        '.zip', '.rar', '.7z',
        # 开发文件
        '.css', '.js', '.map'
    }
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        
        # 只过滤基本的媒体和系统文件
        parsed_url = urlparse(full_url)
        if (parsed_url.netloc == base_domain and 
            not any(path in full_url for path in excluded_paths) and
            not any(full_url.lower().endswith(ext) for ext in excluded_extensions)):
            links.add(full_url)
    
    # 限制返回的链接数量
    return set(list(links)[:MAX_CHILD_PAGES])
