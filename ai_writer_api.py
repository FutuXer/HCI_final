import dashscope

# 建议从环境变量中获取更安全
dashscope.api_key = 'sk-4bda0427e2324d2c9a037fa7c491e12f'

def generate_writing(mode: str, prompt: str) -> str:
    """调用通义千问生成写作内容，支持续写、改写、润色"""
    if mode not in {"扩写", "润色", "续写", "改写"}:
        return f"[错误] 不支持的写作模式：{mode}"

    mode_instruction = {
        "扩写": f"请将以下内容进行扩写，使其更详细生动：{prompt}",
        "润色": f"请润色以下内容，提升语言表达质量：{prompt}",
    }

    response = dashscope.Generation.call(
        model='qwen-turbo',
        messages=[
            {"role": "system", "content": "你是一个中文写作助手，擅长扩写、润色文章。"},
            {"role": "user", "content": mode_instruction[mode]}
        ],
        result_format='message'
    )

    if response and response.status_code == 200:
        return response['output']['choices'][0]['message']['content']
    else:
        return f"[错误] 写作失败：{response.get('code')} - {response.get('message')}"
