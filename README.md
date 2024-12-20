# WaterH Distributor Finder

一个自动化工具，用于寻找适合 WaterH 智能水壶品牌的潜在经销商。

## 功能特点

- 自动搜索并抓取潜在经销商网站
- 分析网站内容和子页面
- 使用 GPT-4 评估经销商适合度
- 生成详细的分析报告

## 安装步骤

1. 克隆仓库：
```bash
git clone [repository-url]
cd waterh-distributor-finder
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 创建并配置 .env 文件：
```bash
# .env
API_KEY=your_openai_api_key
```

## 使用方法

1. 确保已添加 OpenAI API key 到 .env 文件
2. 运行主程序：
```bash
python main.py
```

## 输出说明

- `web_content/`: 存储抓取的网页内容
- `sent_to_chatgpt/`: 存储发送给 GPT 的内容
- `gpt_analysis/`: 存储分析结果（按时间戳命名）
- `log/`: 存储运行日志

## 注意事项

1. **必须配置**: 运行前请确保已在 .env 文件中添加有效的 API_KEY
2. 程序会自动限制抓取速度，避免对目标网站造成压力
3. 分析结果将保存在 gpt_analysis 文件夹中，文件名格式为 YYYYMMDD_HHMM.txt
