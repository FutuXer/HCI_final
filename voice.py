import speech_recognition as sr

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("请开始说话：")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="zh-CN")
        print(f"识别结果：{text}")
        return text
    except sr.UnknownValueError:
        return "语音无法识别"
    except sr.RequestError as e:
        return f"无法连接识别服务: {e}"

