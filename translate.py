import requests
import hashlib
import random


def baidu_translate(q, from_lang='auto', to_lang='zh'):
    appid = '20250610002378073'
    secret_key = 'r86a8d6YhP0BdYDDghIn'
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secret_key
    sign = hashlib.md5(sign.encode()).hexdigest()

    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    params = {
        'q': q,
        'from': from_lang,
        'to': to_lang,
        'appid': appid,
        'salt': salt,
        'sign': sign
    }

    response = requests.get(url, params=params)
    result = response.json()

    if "trans_result" in result:
        return '\n'.join([item['dst'] for item in result['trans_result']])
    else:
        return "翻译失败：" + str(result)


if __name__ == "__main__":
    text = "Hello world!"
    print(baidu_translate(text, 'en', 'zh'))
