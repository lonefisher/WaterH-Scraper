import csv
from googlesearch import search
import os

def fetch_search_results(query, num_results=100, output_file='search_results.csv'):
    """
    Fetch Google search results for a given query and save them to a CSV file.

    Parameters:
        query (str): Search query string.
        num_results (int): Number of search results to fetch.
        output_file (str): Path to the output CSV file.

    Returns:
        None
    """
    try:
        print(f"Searching on Google for: {query}")

        # Create CSV file and write header
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Rank", "URL"])  # Write header

            # Perform Google search and write results
            for rank, url in enumerate(search(query, num_results=num_results, lang="en"), start=1):
                print(f"{rank}. {url}")
                writer.writerow([rank, url])

        print(f"Search results saved to {output_file}.")
    except Exception as e:
        print(f"An error occurred during Google search: {e}")

def process_search_results(input_file, max_results=None):
    """
    处理搜索结果CSV文件
    """
    results = []
    if os.path.exists(input_file):
        with open(input_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # 跳过标题行
            
            for row in csv_reader:
                if len(row) >= 2:
                    rank, url = row
                    if max_results is not None and int(rank) > max_results:
                        break
                    results.append((rank, url))
    return results
