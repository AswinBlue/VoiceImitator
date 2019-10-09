import pyaudio
import queue
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import speech_recognition as sr
from scipy.fftpack import fft

class VoiceRecognizer(object):
    def __init__(self,rate=32768, deviceIdx=1):
        self.__RATE = rate # record rate ,16khz default
        self.__deviceIndex = deviceIdx
        self.__CHUNK = 2048 # buffer size
        self.__pa = pyaudio.PyAudio()
        self.__buffer = queue.Queue()

    def set_recognizer(self):
        self.__r = sr.Recognizer()
        self.__mic = sr.Microphone(device_index = self.__deviceIndex, sample_rate = self.__RATE, chunk_size = self.__CHUNK)
        self.__r.energy_threshold = 500

    def __exit__(self):
        self.__pa.stop_stream()
        self.__pa.close()

    def __fill_buffer(self, in_data, frame_count, time_info, status):
        # print(in_data, frame_count, time_info, status)
        self.__buffer.put(in_data)
        return None, pyaudio.paContinue

    def setGraph(self):
        self.__fig, (ax, ax2) = plt.subplots(2, figsize = (15, 7))
        '''self.fig.canvas.mp1_connect('button_press_event', self.onClick)'''
        x = np.arange(0, 2 * self.__CHUNK, 2)
        self.__line, = ax.plot(x, np.random.rand(self.__CHUNK), '-', lw=2)
        ax.set_title('AUDIO WAVEFORM')
        ax.set_xlabel('time')
        ax.set_ylabel('volume')
        ax.set_ylim(0,255)
        ax.set_xlim(0, self.__CHUNK)
        plt.setp(ax, xticks=[0, self.__CHUNK, 2 * self.__CHUNK], yticks = [0, 128, 255])

        x_fft = np.linspace(0, self.__RATE, self.__CHUNK)
        self.__line_fft, = ax2.semilogx(x_fft, np.random.rand(self.__CHUNK), '-', lw=2)
        ax.set_xlabel('hertz')
        ax.set_ylabel('volume')
        ax2.set_ylim(0, 1)
        ax2.set_xlim(0, 2 * self.__CHUNK)
        ax2.set_xlim(20, self.__RATE / 2)
        plt.setp(ax2, yticks=[0, 1])

        thismanager = plt.get_current_fig_manager()
        thismanager.window.setGeometry(5, 120,1000, 900)
        plt.show(block = False)

    def __drawGraph(self, data):
        data_int = struct.unpack(str(2 * self.__CHUNK) + 'B', data)
        data_np = np.array(data_int, dtype='b')[::2] + 128

        # update ax graph
        self.__line.set_ydata(data_np)

        # update ax2 graph
        y_fft = fft(data_int)
        self.__line_fft.set_ydata(np.abs(y_fft[0:self.__CHUNK]) / (128 * self.__CHUNK))

        # update figure canvas
        self.__fig.canvas.draw()
        self.__fig.canvas.flush_events()

    def pyaudio_set(self) :
        for i in range(self.__pa.get_device_count()):
            print(self.__pa.get_device_info_by_index(i))
        self.stream = self.__pa.open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = self.__RATE,
            input = True,
            frames_per_buffer = self.__CHUNK,
            stream_callback = self.__fill_buffer,
            input_device_index = self.__deviceIndex)

    def pyaudio_listen(self, interval=0.001, iterate=1000):
        self.setGraph()
        for i in range(iterate) :
            # self.stream.read(self.__CHUNK)
            data = self.__buffer.get()

            if data is None :
                return

            self.__drawGraph(data)
            time.sleep(interval)

    def getAverageVolume(self):
        data = np.fromstring(self.stream.read(self.__CHUNK), dtype = np.int16)
        print(int(np.average(np.abs(data))))

    def mic_recognize(self):
        with self.__mic as source:
            self.__r.adjust_for_ambient_noise(source)
            audio = self.__r.listen(source)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }
        try:
            response["transcription"] = self.__r.recognize_google(audio, language = 'ko-KR')
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response