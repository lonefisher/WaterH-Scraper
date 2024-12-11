import os
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from log_utils import setup_logger, log_execution
from config import OUTPUT_FOLDER

# 设置日志记录器
file_manager_logger = setup_logger('file_manager', 'file_manager.log')

# 确保输出文件夹存在
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@log_execution(file_manager_logger)
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

    # Extract text with BeautifulSoup
    text = soup.get_text(separator='\n')  # Preserve structure with \n between tags

    # Preserve up to 2 consecutive newlines, replace others with a single space
    text = re.sub(r'\n{3,}', '\n\n', text)  # Replace 3+ newlines with 2 newlines
    text = re.sub(r'[ \t]+', ' ', text)  # Replace multiple spaces/tabs with a single space
    text = re.sub(r'\n{2,}', '\n\n', text)  # Ensure that no more than 2 newlines exist consecutively
    return text.strip()


@log_execution(file_manager_logger)
def generate_file_path(url, extension='txt'):
    """
    Generate a file path based on the URL and desired extension.

    Parameters:
        url (str): The URL of the website.
        extension (str): The file extension.

    Returns:
        str: The generated file path.
    """
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc.replace(':', '_')  # Replace colons for compatibility
    return os.path.join(OUTPUT_FOLDER, f"{domain_name}.{extension}")


@log_execution(file_manager_logger)
def save_text_to_file(file_path, text_content):
    """
    Save plain text content to a specified file path.

    Parameters:
        file_path (str): Path of the file to save.
        text_content (str): Text content to be saved.

    Returns:
        None
    """
    try:
        with open(file_path, mode='w', encoding='utf-8') as file:
            file.write(text_content)
        file_manager_logger.info(f"Text content successfully saved to {file_path}")
    except Exception as e:
        file_manager_logger.error(f"Failed to save text content to {file_path}. Error: {e}", exc_info=True)
        raise
