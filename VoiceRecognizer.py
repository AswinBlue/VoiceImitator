import pyaudio
import queue
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct

class VoiceRecognizer(object):
    def __init__(self,rate=16000):
        self.__RATE = rate # record rate ,16khz default
        self.__CHUNK = int(self.__RATE / 10) # buffer size
        self.__pa = pyaudio.PyAudio()
        self.__buffer = queue.Queue()

    def __exit__(self):
        self.__pa.stop_stream()
        self.__pa.close()

    def __fill_buffer(self, in_data, frame_count, time_info, status):
        # print(in_data, frame_count, time_info, status)
        self.__buffer.put(in_data)
        return None, pyaudio.paContinue

    def setGraph(self):
        self.__fig, ax = plt.subplots()
        x = np.arange(0, 2 * self.__CHUNK, 2)
        self.__line, = ax.plot(x, np.random.rand(self.__CHUNK))
        ax.set_xlim(0,255)
        ax.set_xlim(0,self.__CHUNK)

    def drawGraph(self, data):
        self.__line.set_ydata(data)
        self.__fig.canvas.draw()
        self.__fig.canvas.flush_events()

    def setStream(self) :
        self.stream = self.__pa.open(
                                format = pyaudio.paInt16,
                                channels = 1,
                                rate = self.__RATE,
                                input = True,
                                output = True,
                                frames_per_buffer = self.__CHUNK,
                                stream_callback = self.__fill_buffer,
                                input_device_index = 1)

    def listen(self, interval=0.1, iterate=1000):
        self.setGraph()
        for i in range(iterate) :
            # self.stream.read(self.__CHUNK)
            data = self.__buffer.get()

            if data is None :
                return

            data_int = np.array(struct.unpack(str(2 * self.__CHUNK) + 'B', data), dtype='b')[::2] + 127
            print(data_int)
            self.drawGraph(data_int)

            time.sleep(interval)

    def getAverageVolume(self):
        data = np.fromstring(self.stream.read(self.__CHUNK), dtype = np.int16)
        print(int(np.average(np.abs(data))))

