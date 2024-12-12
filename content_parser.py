from bs4 import BeautifulSoup
import re
from log_utils import setup_logger, log_execution

# 设置日志记录器
content_parser_logger = setup_logger('content_parser', 'content_parser.log')


@log_execution(content_parser_logger)
def extract_text_from_html(html_content):
    """
    Extract plain text from HTML using BeautifulSoup and clean it up:
    - Preserve paragraph structure by keeping up to 2 consecutive newlines.
    - Replace extra spaces and single newlines with a single space.

    Parameters:
        html_content (str): Raw HTML content.

    Returns:
        str: Cleaned text extracted from the HTML.
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 删除更多不需要的HTML元素
        unwanted_elements = [
            'nav', 'header', 'footer', 'script', 'style', 'meta', 'link', 
            'iframe', 'form', 'button', 'aside', 'noscript', 'svg', 'path',
            'img', 'picture', 'video', 'audio', 'canvas', 'map', 'object',
            'menu', 'dialog', 'select', 'option'
        ]
        
        unwanted_classes = [
            'menu', 'nav', 'header', 'footer', 'sidebar', 'cookie', 'popup',
            'banner', 'social', 'cart', 'search', 'breadcrumb', 'pagination',
            'widget', 'advertisement', 'share', 'modal', 'overlay', 'drawer',
            'newsletter', 'subscribe', 'login', 'auth', 'account', 'toolbar'
        ]
        
        # 安全地删除标签
        for tag in unwanted_elements:
            for element in soup.find_all(tag):
                if element:  # 确保元素存在
                    element.decompose()
        
        # 安全地删除带特定class的元素
        for element in soup.find_all(class_=True):
            if element and element.get('class'):  # 确保元素和class属性存在
                element_classes = [str(cls).lower() for cls in element.get('class', [])]
                if any(unwanted in element_classes for unwanted in unwanted_classes):
                    element.decompose()
                
        # 安全地删除空白标签
        for element in soup.find_all():
            if element and not element.get_text(strip=True):  # 确保元素存在
                element.decompose()
        
        # 提取文本并清理
        if soup.body:  # 优先从body提取
            text = soup.body.get_text(separator='\n')
        else:
            text = soup.get_text(separator='\n')
            
        # 调用去重函数
        return remove_duplicates_from_text(text)
        
    except Exception as e:
        print(f"Error in extract_text_from_html: {str(e)}")
        return ""  # 返回空字符串而不是None

def remove_duplicates_from_text(text):
    """
    高级文本去重和清理，专门针对电商网站内容
    """
    # 按行分割
    lines = text.split('\n')
    
    # 扩展过滤模式
    skip_patterns = {
        # 导航相关
        'Show submenu for', 'Skip to content', 'Quick Links', 'Main Menu', 'Navigation',
        'Menu', 'Submenu', 'Toggle navigation', 'Toggle menu', 'Open menu', 'Close menu',
        
        # 页脚常见元素
        'Terms & Conditions', 'Privacy Notice', 'Cookie Policy', 'All rights reserved',
        'Contact Us', 'About Us', 'FAQ', 'Help', 'Support', 'Sitemap', 'Newsletter',
        'Subscribe', 'Sign up', 'Log in', 'Register', 'My Account',
        
        # 社交媒体相关
        'Follow us', 'Share on', 'Find us on', 'Connect with us', 'Social Media',
        'Facebook', 'Twitter', 'Instagram', 'LinkedIn', 'YouTube',
        
        # 电商常见元素
        'Add to cart', 'Buy now', 'Shopping cart', 'Checkout', 'Basket',
        'Wishlist', 'Save for later', 'In stock', 'Out of stock', 'Delivery',
        'Returns', 'Payment', 'Shipping',
        
        # 注册和法律信息
        'Registered in', 'VAT No', 'WEEE Reg No', 'Company Number',
        'Copyright', '© 20', 'All Rights Reserved', 'Privacy Policy',
        
        # 搜索相关
        'Search', 'Search results', 'No results found', 'Advanced search',
        
        # 其他通用元素
        'Back to top', 'Read more', 'Learn more', 'View details',
        'Next', 'Previous', 'Page', 'Loading'
    }
    
    def clean_line(line):
        """清理和标准化文本行"""
        # 移除多余空白
        line = ' '.join(line.split())
        # 移除特殊字符
        line = re.sub(r'[^\w\s\-.,;:?!()"\'£$€%&@#*+=/\\]', '', line)
        return line.strip()
    
    def is_meaningful_content(line):
        """判断是否是有意义的内容"""
        # 移除空白字符后的长度
        clean_length = len(''.join(line.split()))
        # 字母数字字符的比例
        alnum_ratio = sum(c.isalnum() for c in line) / len(line) if line else 0
        
        return (
            clean_length >= 3 and  # 至少3个非空白字符
            alnum_ratio >= 0.3 and  # 至少30%是字母数字
            not line.isdigit() and  # 不是纯数字
            not all(c.isupper() for c in line.replace(' ', ''))  # 不是纯大写
        )
    
    def should_skip_line(line):
        """判断是否应该跳过该行"""
        if not line or len(line.strip()) < 2:
            return True
            
        # 跳过包含跳过模式的行
        if any(pattern.lower() in line.lower() for pattern in skip_patterns):
            return True
            
        # 跳过常见的无意义行
        if not is_meaningful_content(line):
            return True
            
        # 跳过URL和邮箱
        if re.match(r'^(https?:|www\.|mailto:)', line.lower()):
            return True
            
        return False
    
    # 存储已处理的内容
    processed_content = []
    seen_content = set()
    
    current_section = []
    
    for line in lines:
        line = clean_line(line)
        
        if should_skip_line(line):
            continue
        
        # 处理产品特性列表
        if line.startswith(('- ', '• ', '* ')):
            current_section.append(line)
            continue
            
        # 处理标题或新段落
        if len(line) > 40 or line.endswith((':',)):
            if current_section:
                section_text = '\n'.join(current_section)
                if section_text not in seen_content:
                    processed_content.append(section_text)
                    seen_content.add(section_text)
                current_section = []
            
            if line not in seen_content:
                processed_content.append(line)
                seen_content.add(line)
        else:
            current_section.append(line)
    
    # 处理最后一个段落
    if current_section:
        section_text = '\n'.join(current_section)
        if section_text not in seen_content:
            processed_content.append(section_text)
    
    # 组合最终文本
    final_text = '\n\n'.join(processed_content)
    
    # 最终清理
    final_text = re.sub(r'\n{3,}', '\n\n', final_text)  # 删除多余空行
    final_text = re.sub(r' {2,}', ' ', final_text)      # 删除多余空格
    
    return final_text.strip()
