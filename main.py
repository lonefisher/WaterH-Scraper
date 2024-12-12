import os
import csv
from web_scraper import fetch_html_content, extract_same_domain_links
from file_manager import save_webpage_content, save_chatgpt_content
from content_parser import extract_text_from_html
from model_analyzer import analyze_with_model
from config import MAX_RESULTS, PROMPT_TEMPLATE, MAX_CHILD_PAGES

def process_url(rank, url):
    """
    处理单个URL及其子页面
    """
    try:
        print(f"\nProcessing rank {rank}, URL: {url}")
        
        # 获取主页面内容
        main_html = fetch_html_content(url)
        main_text = extract_text_from_html(main_html)
        
        # 提取同域名链接
        child_links = extract_same_domain_links(main_html, url)
        child_contents = {}
        
        # 获取子页面内容
        for child_url in list(child_links)[:MAX_CHILD_PAGES]:
            try:
                print(f"  Fetching child URL: {child_url}")
                child_html = fetch_html_content(child_url)
                child_text = extract_text_from_html(child_html)
                child_contents[child_url] = child_text
            except Exception as e:
                print(f"  Failed to fetch child URL: {child_url}. Error: {e}")
                continue
        
        # 保存网页内容
        save_webpage_content(url, main_text, child_contents)
        
        # 组合内容用于ChatGPT分析
        combined_content = f"Main site {url}:\n{main_text}\n\n"
        for child_url, content in child_contents.items():
            combined_content += f"Child site {child_url}:\n{content}\n\n"
        
        # 保存发送给ChatGPT的内容
        save_chatgpt_content(url, combined_content)
        
        # 分析内容
        modified_prompt = PROMPT_TEMPLATE.format(content=combined_content)
        analysis_result = analyze_with_model(modified_prompt)
        
        print(f"\nAnalysis result for URL rank {rank} ({url}):\n{analysis_result}\n")
        return analysis_result
        
    except Exception as e:
        print(f"Failed to process URL rank {rank}, URL: {url}. Error: {str(e)}")
        return None

def fetch_search_results(query):
    """
    使用Google搜索获取结果并保存到CSV
    """
    try:
        from googlesearch import search
        results = []
        for i, url in enumerate(search(query, num_results=MAX_RESULTS), 1):
            results.append([i, url])
        
        with open('search_results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Rank', 'URL'])
            writer.writerows(results)
            
    except Exception as e:
        print(f"Failed to fetch search results: {str(e)}")

def main():
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
            next(csv_reader)  # 跳过标题行

            for row in csv_reader:
                if len(row) >= 2:  # 确保行包含足够的列
                    rank, url = row
                    if MAX_RESULTS is not None and int(rank) > MAX_RESULTS:
                        break
                    process_url(rank, url)

if __name__ == "__main__":
    main()
