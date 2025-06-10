from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import time
from aip import AipSpeech
import pyaudio
import wave
import os
import speech_recognition as sr  # 补充缺失的import


class VoiceInputThread(QThread):
    result_ready = pyqtSignal(str)
    status_update = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.recognizer = sr.Recognizer()  # 初始化语音识别器

        # 百度语音API配置
        self.APP_ID = '6927050'
        self.API_KEY = 'vtXVCLNnGAU348EVajXm5PZF'
        self.SECRET_KEY = 'lG439CVdi9Kd4VDfCa52yjTMvbjtJdAy'
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

        # 音频参数（保持5秒截断）
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.MAX_RECORD_SECONDS = 5  # 保持5秒录音
        self.WAVE_OUTPUT_FILENAME = "temp_audio.wav"

    def stop(self):
        self.running = False
        if not self.wait(3000):  # 3秒自动退出
            self.terminate()
        self.status_update.emit("🛑 语音识别已停止")

    def record_audio(self):
        """保持原有5秒录音逻辑"""
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        self.status_update.emit("🎤 正在录音...请说话")
        frames = []

        for _ in range(0, int(self.RATE / self.CHUNK * self.MAX_RECORD_SECONDS)):
            if not self.running:
                break
            data = stream.read(self.CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(self.WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))

        return self.WAVE_OUTPUT_FILENAME

    def recognize_audio(self, audio_file):
        """带超时控制的识别"""
        with open(audio_file, 'rb') as f:
            audio_data = f.read()

        # 百度API的5秒超时保持不变
        result = self.client.asr(audio_data, 'wav', self.RATE, {
            'dev_pid': 1537
        })

        if os.path.exists(audio_file):
            os.remove(audio_file)

        if result.get('err_no') != 0:
            # 特殊处理静默超时错误（错误码2001）
            if result['err_no'] == 2001:
                raise sr.UnknownValueError("未检测到语音输入")
            raise Exception(f"百度API错误: {result.get('err_msg')}")

        return result.get('result')[0]

    def run(self):
        try:
            while self.running:
                try:
                    self.status_update.emit("正在准备录音设备...")
                    audio_file = self.record_audio()

                    if not self.running:
                        break

                    self.status_update.emit("🔍 正在识别语音...")
                    start_time = time.time()

                    text = self.recognize_audio(audio_file)
                    processing_time = round(time.time() - start_time, 2)

                    self.status_update.emit(f"✅ 识别完成 (耗时 {processing_time}s)")
                    self.result_ready.emit(text)

                except sr.UnknownValueError:
                    if self.running:
                        self.error_occurred.emit("❌ 未检测到语音输入")
                    continue
                except Exception as e:
                    if self.running:
                        self.error_occurred.emit(f"⚠️ 发生错误: {str(e)}")
                    continue

        finally:
            if os.path.exists(self.WAVE_OUTPUT_FILENAME):
                os.remove(self.WAVE_OUTPUT_FILENAME)
