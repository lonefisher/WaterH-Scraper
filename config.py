# config.py

# 文件夹配置
OUTPUT_FOLDER = 'web_content'  # 存储网页内容的文件夹
LOG_FOLDER = 'log'  # 存储日志的文件夹

# 网页抓取配置
MAX_RESULTS =3  # 限制要抓取的网页数量
SEARCH_QUERY = "lifestyle distribution consumer electronics uk"  # 搜索关键词
SEARCH_NUM_RESULTS = 100  # Google 搜索结果数量

# OpenAI API 配置
API_BASE = 'https://open.xiaojingai.com/v1'
MODEL = 'gpt-4o-mini'
MAX_TOKENS = 1000  # 最大生成的 token 数量

# Prompt 模板
PROMPT_TEMPLATE = """
Based on the following website content, determine if the company qualifies as a potential distributor for WaterH, a smart water bottle brand. Use the following criteria:

1. Does the company showcase brands related to WaterH’s product field? Examples include BlendJet, Laifen, Ember, Owala, Montigo, Klean Kanteen, Simple Modern, Larq, Hidrate Spark, Outin, Nano Leaf, Ringo, Oura Ring, or similar brands in water bottles or smart wearables.
2. If no such brands are mentioned, does the company operate in relevant sectors like smart products, outdoor gear, or consumer electronics, which could overlap with the smart water bottle market?

### Your Response:
1. **Answer:** "Yes," "No," or "Uncertain" to indicate whether the company qualifies as a potential distributor.
2. **Reason:** Provide a brief explanation of your reasoning.

#### Example Output:
- Answer: Yes  
  Reason: The website lists brands like Larq and Ember, which are relevant to WaterH’s category.   

Website Content:
{content}
"""
