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
    提取与主域名相同的有效链接，排除媒体文件和其他无关格式
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    base_domain = urlparse(base_url).netloc
    links = set()
    
    # 定义要排除的文件扩展名
    excluded_extensions = {
        # 图片格式
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.ico', '.tiff', '.webp', '.heic',
        
        # 视频格式
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.m4v', '.mpeg', '.mpg',
        
        # 音频格式
        '.mp3', '.wav', '.ogg', '.m4a', '.wma', '.aac', '.flac', '.mid', '.midi',
        
        # 文档格式
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp',
        '.rtf', '.txt', '.csv', '.xml', '.json',
        
        # 压缩文件
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
        
        # 开发相关
        '.css', '.js', '.jsx', '.ts', '.tsx', '.map', '.php', '.asp', '.aspx', '.jsp',
        '.py', '.rb', '.java', '.class', '.dll', '.exe', '.apk', '.ipa',
        
        # 字体文件
        '.ttf', '.otf', '.woff', '.woff2', '.eot',
        
        # 其他二进制格式
        '.bin', '.dat', '.db', '.sql', '.sqlite'
    }
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        
        # 检查是否为相同域名且不是被排除的文件类型
        parsed_url = urlparse(full_url)
        if (parsed_url.netloc == base_domain and 
            not any(full_url.lower().endswith(ext) for ext in excluded_extensions) and
            not full_url.endswith('/wp-content/') and  # 排除WordPress媒体目录
            not '/wp-content/uploads/' in full_url and  # 排除WordPress上传目录
            not '/assets/' in full_url and  # 排除常见的资源目录
            not '/images/' in full_url and  # 排除图片目录
            not '/downloads/' in full_url):  # 排除下载目录
            links.add(full_url)
    
    return links
