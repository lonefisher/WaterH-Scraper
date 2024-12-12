# config.py

# 文件夹配置
OUTPUT_FOLDER = 'web_content'  # 存储网页内容的文件夹
LOG_FOLDER = 'log'  # 存储日志的文件夹
CHATGPT_OUTPUT_FOLDER = 'sent_to_chatgpt'  # 存储发送给ChatGPT的内容的文件夹
GPT_ANALYSIS_FOLDER = 'gpt_analysis'  # 存储GPT分析结果的文件夹

# 网页抓取配置
MAX_RESULTS =100  # 限制要抓取的网页数量
SEARCH_QUERY = "lifestyle distribution consumer electronics uk"  # 搜索关键词
SEARCH_NUM_RESULTS = 100  # Google 搜索结果数量
MAX_CHILD_PAGES = 999  # 每个主页面最多抓取的子页面数量

# OpenAI API 配置
API_BASE = 'https://open.xiaojingai.com/v1'
MODEL = 'gpt-4o-mini'
MAX_TOKENS = 128000  # gpt-4o-mini的实际上下文窗口大小

PROMPT_TEMPLATE = """
Based on the following website content (including main site and child pages), evaluate if the company would be a suitable distributor for WaterH smart water bottle brand. Please analyze using these criteria:

1. Brand Relevance:
   - Does the company distribute brands related to WaterH's product field? Relevant brand examples include: BlendJet, Laifen, Ember, Owala, Montigo, Klean Kanteen, Simple Modern, Larq, Hidrate Spark, Outin, Nano Leaf, Ringo, Oura Ring, or similar brands in water bottles or smart wearables.

2. Market Sectors:
   - If none of the above brands are mentioned, does the company operate in relevant sectors such as smart products, outdoor gear, or consumer electronics that could overlap with the smart water bottle market?

Website Content:
{content}

### Your Response:
1. **Answer:** "Yes," "No," or "Uncertain" to indicate whether the company qualifies as a potential distributor.
2. **Reason:** Provide a brief explanation of your reasoning based on both main and child pages content.
"""
