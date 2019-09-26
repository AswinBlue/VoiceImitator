import VoiceRecognizer

if __name__ == '__main__' :
    print('start program')
    vr = VoiceRecognizer.VoiceRecognizer()

    vr.setStream()
    for i in range(1000) :
        vr.getAverageVolume()
    print('start finish')

