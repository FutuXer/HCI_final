# qwen_writer_api.py
import dashscope

# 替换成你的 AccessKey（建议放到环境变量）
dashscope.api_key = 'sk-4bda0427e2324d2c9a037fa7c491e12f'

def generate_writing(prompt):
    """调用通义千问生成写作内容"""
    response = dashscope.Generation.call(
        model='qwen-turbo',
        messages=[
            {"role": "system", "content": "你是一个中文写作助手，擅长扩写、润色、续写文章。"},
            {"role": "user", "content": f"请根据下面内容扩写一段文字：{prompt}"}
        ],
        result_format='message'
    )

    if response and response.status_code == 200:
        return response['output']['choices'][0]['message']['content']
    else:
        return f"[错误] 写作失败：{response.get('code')} - {response.get('message')}"
