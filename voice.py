from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import time
from aip import AipSpeech
import pyaudio
import wave
import os
import speech_recognition as sr


class VoiceInputThread(QThread):
    result_ready = pyqtSignal(str)
    status_update = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mutex = QMutex()  # 正确初始化互斥锁
        self._running = False  # 统一使用一个运行标志

        # 初始化识别器
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8  # 设置静音检测阈值

        # 百度语音API配置
        self.APP_ID = '6927050'
        self.API_KEY = 'vtXVCLNnGAU348EVajXm5PZF'
        self.SECRET_KEY = 'lG439CVdi9Kd4VDfCa52yjTMvbjtJdAy'
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

        # 音频参数
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.WAVE_OUTPUT_FILENAME = "temp_audio.wav"

    def recognize_audio(self, audio_file):
        if audio_file is None:
            raise Exception("无有效音频输入")
        """使用百度语音API识别音频文件"""
        try:
            # 读取音频文件
            with open(audio_file, 'rb') as audio_data:
                audio_content = audio_data.read()

            # 调用百度语音识别API（修正参数格式）
            result = self.client.asr(
                audio_content,
                'wav',
                16000, {
                    'dev_pid': 1537  # 1537表示普通话(纯中文识别)
                }
            )

            # 检查识别结果
            if result.get('err_no') != 0:
                error_msg = result.get('err_msg', '未知错误')
                # 特殊处理静音超时错误(错误码2001)
                if result['err_no'] == 2001:
                    raise sr.UnknownValueError("未检测到语音输入")
                raise Exception(f"百度API错误: {error_msg}")

            # 返回识别结果
            if 'result' in result and len(result['result']) > 0:
                return result['result'][0]
            else:
                raise Exception("未识别到有效内容")

        except sr.UnknownValueError:
            raise Exception("无法识别语音内容")
        except sr.RequestError as e:
            raise Exception(f"语音识别服务错误: {str(e)}")
        except Exception as e:
            raise Exception(f"识别过程中发生错误: {str(e)}")

    def stop(self):
        self.mutex.lock()
        self._running = False
        self.mutex.unlock()
        self.status_update.emit("🛑 已停止")
        self.wait()  # 阻塞等待线程结束，确保线程完全退出后再返回

    def run(self):
        self.mutex.lock()
        self._running = True
        self.mutex.unlock()

        try:
            from ui.resources import AudioManager
            audio = AudioManager()

            self.status_update.emit("🎤 正在录音...请说话")

            stream = audio.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )

            frames = []

            while True:
                self.mutex.lock()
                running = self._running
                self.mutex.unlock()

                if not running:
                    break

                data = stream.read(self.CHUNK)
                frames.append(data)

                # 这里可以加个限制最长录音时间，例如10秒，防止死循环
                if len(frames) >= int(self.RATE / self.CHUNK * 10):
                    break

            stream.stop_stream()
            stream.close()

            if frames:
                with wave.open(self.WAVE_OUTPUT_FILENAME, 'wb') as wf:
                    wf.setnchannels(self.CHANNELS)
                    wf.setsampwidth(audio.p.get_sample_size(self.FORMAT))
                    wf.setframerate(self.RATE)
                    wf.writeframes(b''.join(frames))

                self.status_update.emit("识别中...")
                text = self.recognize_audio(self.WAVE_OUTPUT_FILENAME)
                self.result_ready.emit(text)

        except Exception as e:
            self.error_occurred.emit(f"识别错误: {str(e)}")
        finally:
            self.status_update.emit("准备就绪")
            if os.path.exists(self.WAVE_OUTPUT_FILENAME):
                os.remove(self.WAVE_OUTPUT_FILENAME)
