import openai
from config import API_BASE, MODEL, PROMPT_TEMPLATE
from log_utils import setup_logger, log_execution
from dotenv import load_dotenv
import os

load_dotenv()
# 设置日志记录器
model_analyzer_logger = setup_logger('model_analyzer', 'model_analyzer.log')
API_KEY = os.getenv('API_KEY')
# 配置 OpenAI API
openai.api_key = API_KEY
openai.api_base = API_BASE

@log_execution(model_analyzer_logger)
def analyze_with_model(content, prompt_template=PROMPT_TEMPLATE, model=MODEL):
    """
    Analyze content using a specified OpenAI model and prompt template.

    Parameters:
        content (str): The text content to be analyzed.
        prompt_template (str): The prompt template used to generate the analysis.
        model (str): The OpenAI model to be used.

    Returns:
        str: The analysis result from the model.
    """
    try:
        # Format the prompt with the provided content
        prompt = prompt_template.format(content=content)

        # Log the formatted prompt (truncated for readability)
        model_analyzer_logger.info(f"Formatted prompt: {prompt[:500]}...")  # Limit log to 500 characters

        # Call the OpenAI model
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a skilled assistant analyzing websites for potential distributors."},
                {"role": "user", "content": prompt}
            ],
            temperature=0  # Deterministic results for consistency
        )

        # Extract and return the analysis result
        result = response['choices'][0]['message']['content'].strip()
        model_analyzer_logger.info(f"Model analysis result: {result[:500]}...")  # Log result (truncated)
        return result

    except openai.error.OpenAIError as e:
        model_analyzer_logger.error(f"OpenAI API error: {e}", exc_info=True)
        raise
    except Exception as e:
        model_analyzer_logger.error(f"Unexpected error in analyze_with_model: {e}", exc_info=True)
        raise
