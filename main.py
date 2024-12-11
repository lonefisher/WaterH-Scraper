import csv
import os
from web_scraper import fetch_html_content
from file_manager import extract_text_from_html, generate_file_path, save_text_to_file
from model_analyzer import analyze_with_model
from config import MAX_RESULTS
from scrap_link_from_google import fetch_search_results  # 导入抓取模块

def process_url(rank, url):
    """
    Process a single URL: fetch, save, and analyze.
    """
    try:
        # Step 1: Fetch HTML content from the URL
        html_content = fetch_html_content(url)

        # Step 2: Extract plain text from the HTML content
        text_content = extract_text_from_html(html_content)

        # Step 3: Generate a file path to save the extracted content
        file_path = generate_file_path(url)

        # Step 4: Save the extracted content to a file
        save_text_to_file(file_path, text_content)

        # Step 5: Analyze the text content using the OpenAI model
        analysis_result = analyze_with_model(text_content)

        # Step 6: Print the analysis result with the URL
        print(f"Analysis result for URL rank {rank} ({url}):\n{analysis_result}\n")

    except Exception as e:
        print(f"Failed to process URL rank {rank}, URL: {url}. Error: {e}")

if __name__ == "__main__":
    input_file = 'search_results.csv'
    query = "lifestyle distribution consumer electronics uk"  # 搜索关键词

    # 检查是否存在 CSV 文件
    if not os.path.exists(input_file):
        print(f"{input_file} not found. Running Google search to generate it...")
        fetch_search_results(query)

    # 处理 CSV 文件中的 URL
    if os.path.exists(input_file):
        with open(input_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row

            for rank, url in csv_reader:
                if MAX_RESULTS is not None and int(rank) > MAX_RESULTS:
                    break
                process_url(rank, url)
