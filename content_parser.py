from bs4 import BeautifulSoup
from log_utils import setup_logger, log_execution

# 设置日志记录器
content_parser_logger = setup_logger('content_parser', 'content_parser.log')


@log_execution(content_parser_logger)
def extract_text_from_html(html_content):
    """
    从HTML内容中提取纯文本
    """
    if not html_content:
        return ""
        
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 移除脚本和样式元素
        for element in soup(['script', 'style', 'head', 'title', 'meta', '[document]']):
            element.decompose()
        
        # 获取文本
        text = soup.get_text(separator='\n', strip=True)
        
        # 清理文本
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except Exception as e:
        content_parser_logger.error(f"Error in extract_text_from_html: {str(e)}")
        return ""
