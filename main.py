import VoiceRecognizer

if __name__ == '__main__' :
    print('start program')
    vr = VoiceRecognizer.VoiceRecognizer()

    # vr.setStream()
    # vr.pyaudio_listen()
    vr.set_recognizer()
    vr.mic_recognize()
    print('start finish')

