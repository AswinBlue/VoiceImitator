import pyaudio
import queue
import numpy as np

class VoiceRecognizer(object):
    def __init__(self,rate=16000):
        self.__RATE = rate # record rate ,16khz default
        self.__CHUNK = int(self.__RATE / 10) # buffer size
        self.__pa = pyaudio.PyAudio()
        self.__buffer = queue.Queue()

    def __exit__(self):
        self.__pa.stop_stream()
        self.__pa.close()

    def __fill_buffer(self, in_data, frame_count, time_info, status_flag):
        self.__buffer.put(in_data)
        print(in_data, frame_count, time_info, status_flag)
        return None, pyaudio.paContinue

    def setStream(self) :
        self.stream = self.__pa.open(format = pyaudio.paInt16,
                                channels = 1,
                                rate = self.__RATE,
                                input = True,
                                frames_per_buffer = self.__CHUNK,
                                stream_callback = self.__fill_buffer,
                                input_device_index = 2)

    def listen(self, interval=0.1):
        while True :
            chunk = self.__buffer.get(block = False)
            if chunk is None :
                return
            yield b''.join([chunk])
            bufferAdded = False
            time.sleep(interval)

    def getAverageVolume(self):
        data = np.fromstring(self.stream.read(self.__CHUNK), dtype = np.int16)
        print(int(np.average(np.abs(data))))

