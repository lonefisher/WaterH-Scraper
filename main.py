import os
from scrap_link_from_google import fetch_search_results, process_search_results
from web_scraper import process_website
from file_manager import save_webpage_content, save_chatgpt_content, save_gpt_analysis
from model_analyzer import analyze_with_model
from config import MAX_RESULTS, PROMPT_TEMPLATE, SEARCH_QUERY, SEARCH_NUM_RESULTS

def main():
    input_file = 'search_results.csv'
    
    # 如果不存在搜索结果，执行搜索
    if not os.path.exists(input_file):
        fetch_search_results(SEARCH_QUERY, SEARCH_NUM_RESULTS, input_file)
    
    # 处理搜索结果
    for rank, url in process_search_results(input_file, MAX_RESULTS):
        try:
            # 删除这行重复的输出
            # print(f"\nProcessing rank {rank}, URL: {url}")
            
            # 处理网站内容
            main_text, child_contents = process_website(rank, url)
            if main_text is None:
                continue
                
            # 保存网页内容
            save_webpage_content(url, main_text, child_contents)
            
            # 准备和分析内容
            combined_content = prepare_content(url, main_text, child_contents)
            save_chatgpt_content(url, combined_content)
            
            # GPT分析
            analysis_result = analyze_content(combined_content)
            save_gpt_analysis(rank, url, analysis_result)
            
            # 打印分析结果
            print(f"\nAnalysis result for URL rank {rank} ({url}):")
            print(analysis_result)
            print("\n" + "="*50)
            
        except Exception as e:
            print(f"Error processing URL rank {rank}: {str(e)}")
            continue

def prepare_content(url, main_text, child_contents):
    """准备发送给GPT的内容"""
    combined_content = f"Main site {url}:\n{main_text}\n\n"
    for child_url, content in child_contents.items():
        if content.strip():
            combined_content += f"Child site {child_url}:\n{content}\n\n"
    return combined_content

def analyze_content(combined_content):
    """分析内容"""
    print("\nSending to GPT for analysis...")
    modified_prompt = PROMPT_TEMPLATE.format(content=combined_content)
    analysis_result = analyze_with_model(modified_prompt)
    return analysis_result

if __name__ == "__main__":
    main()
