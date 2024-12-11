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
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract text and clean up extra newlines and spaces
    text = soup.get_text(separator='\n')  # Preserve structure with \n between tags
    text = re.sub(r'\n{3,}', '\n\n', text)  # Replace 3+ newlines with 2 newlines
    text = re.sub(r'[ \t]+', ' ', text)  # Replace multiple spaces/tabs with a single space
    return text.strip()
