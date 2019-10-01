import VoiceRecognizer

if __name__ == '__main__' :
    print('start program')
    vr = VoiceRecognizer.VoiceRecognizer()

    vr.setStream()
    vr.listen()
    print('start finish')

