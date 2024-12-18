import requests
from log_utils import setup_logger, log_execution
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from config import MAX_CHILD_PAGES
from content_parser import extract_text_from_html

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

def process_website(rank, url):
    """
    处理单个网站及其子页面
    """
    try:
        print(f"\nProcessing rank {rank}, URL: {url}")
        
        # 获取主页面内容
        main_html = fetch_html_content(url)
        main_text = extract_text_from_html(main_html)
        
        # 提取同域名链接
        child_links = extract_same_domain_links(main_html, url)
        
        # 处理子页面内容
        child_contents = process_child_pages(child_links)
        
        return main_text, child_contents
        
    except Exception as e:
        print(f"Failed to process URL rank {rank}, URL: {url}. Error: {e}")
        return None, None

def process_child_pages(child_links):
    """
    处理子页面
    """
    child_contents = {}
    for child_url in list(child_links)[:MAX_CHILD_PAGES]:
        try:
            print(f"  Fetching child URL: {child_url}")
            child_html = fetch_html_content(child_url)
            child_text = extract_text_from_html(child_html)
            if child_text.strip():
                child_contents[child_url] = child_text
                
        except Exception as e:
            print(f"  Failed to fetch child URL: {child_url}. Error: {e}")
            continue
    return child_contents
