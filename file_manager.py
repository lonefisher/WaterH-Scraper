import os
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from log_utils import setup_logger, log_execution
from config import OUTPUT_FOLDER, CHATGPT_OUTPUT_FOLDER
from content_parser import remove_duplicates_from_text

# 设置日志记录器
file_manager_logger = setup_logger('file_manager', 'file_manager.log')

def sanitize_filename(url):
    """
    将URL转换为安全的文件名
    - 移除协议前缀 (http://, https://)
    - 将特殊字符替换为下划线
    - 限制长度
    """
    # 移除协议前缀
    url = re.sub(r'^https?://', '', url)
    # 替换特殊字符
    url = re.sub(r'[\\/:*?"<>|]', '_', url)
    # 限制长度（保留最后100个字符）
    if len(url) > 100:
        url = url[-100:]
    return url

def save_webpage_content(base_url, main_content, child_contents):
    """
    保存主页面和子页面内容，文件名包含URL信息
    
    Args:
        base_url (str): 主URL
        main_content (str): 主页面内容
        child_contents (dict): 子页面内容字典 {url: content}
    """
    # 创建基本目录
    domain = urlparse(base_url).netloc
    base_path = os.path.join(OUTPUT_FOLDER, domain)
    os.makedirs(base_path, exist_ok=True)
    
    # 保存主页面内容
    main_filename = f'main-url_{sanitize_filename(base_url)}.txt'
    with open(os.path.join(base_path, main_filename), 'w', encoding='utf-8') as f:
        f.write(f"URL: {base_url}\n\n")  # 在文件开头写入URL
        f.write(main_content)
    
    # 保存子页面内容
    for i, (url, content) in enumerate(child_contents.items(), 1):
        child_filename = f'child-url-{i}_{sanitize_filename(url)}.txt'
        with open(os.path.join(base_path, child_filename), 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n\n")  # 在文件开头写入URL
            f.write(content)

def save_chatgpt_content(base_url, combined_content):
    """
    保存发送给ChatGPT的内容
    """
    domain = urlparse(base_url).netloc
    os.makedirs(CHATGPT_OUTPUT_FOLDER, exist_ok=True)
    
    filename = f'{domain}_{sanitize_filename(base_url)}.txt'
    filepath = os.path.join(CHATGPT_OUTPUT_FOLDER, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(combined_content)

@log_execution(file_manager_logger)
def extract_text_from_html(html_content):
    """
    从HTML中提取文本并去重
    """
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator='\n')
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{2,}', '\n\n', text)
    text = text.strip()
    
    # 调用去重函数
    text = remove_duplicates_from_text(text)
    
    return text
