import sounddevice as sd
import numpy as np
import pydirectinput
import sys

##tabela de frequências do Fernando Iazzetta https://iazzetta.eca.usp.br/tutor/acustica/introducao/tabela1.html
##primeiro lá da flauta -> 440Hz

fs = 44100 # frequência de amostragem
duration = 0.4  # segundos

##print(sd.query_devices()) ##ver microfones
##sd.default.device = 1, 1     ##escolher microfones

def recording():
    try:
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        musicNote = fourier(myrecording)
        print(musicNote)
        pressKey(musicNote)
        return 

    except Exception as e:
        print("Erro na função recording:", e)

def pressKey(frequency):
    try:
        if 256 < frequency < 266:
            pydirectinput.keyUp('down')
            return
        elif 288< frequency < 298:
            pydirectinput.keyDown('down')
            return
        elif 324 < frequency < 334:
            pydirectinput.press('down')
            return
        elif 339 < frequency < 359:
            pydirectinput.keyUp('left')
            return
        elif 381 < frequency < 401:
            pydirectinput.keyDown('left')
        elif 405 < frequency < 425:
            pydirectinput.press('left')
        elif 430 < frequency < 450: 
            pydirectinput.keyDown('right')
            return
        elif 483 < frequency < 503: 
            pydirectinput.keyUp('right')
            return
        elif 513 < frequency < 533:
            pydirectinput.press('right')
            return
        elif 773 < frequency < 793: 
            pydirectinput.press('a')
            return
        ##elif 870 < frequency < 890:
            ##pydirectinput.keyDown('up')
            ##return
        ##elif 977 < frequency < 997:
            ##pydirectinput.keyUp('up')
            ##return
        elif 1164 < frequency < 1194:
            pydirectinput.press('enter')
            return
        else:
            pass
    except Exception as e:
        print("Erro na função pressKey:", e)

def fourier(recording):
    try: 
        N = len(recording)
        T = 1/fs #Período de amostragem
        freq = np.fft.fftfreq(N, T)[:N//2]  #indices das frequencias de fourier 
        mag = np.abs(np.fft.fft(recording.flatten()))[:N//2] #magnitudes das transformadas de fourier

        ##limitar as frequencias entre 20 e 20khz, pois são as únicas úteis para som
        mask = (freq >= 20) & (freq <= 20000)
        freqFiltered = freq[mask]
        magFiltered = mag[mask]

        domFreqIndex = np.argmax(magFiltered) #Pega o index da magnitude máxima
        finalFreq = freqFiltered[domFreqIndex]  #A frequencia maxima do intervalo gravado 

        return finalFreq 

    except Exception as e:
        print("Erro na função fourier:", e)

try:
    while True:
        try:    
            recording()
        except Exception as e:
            print("Erro:", e)

except KeyboardInterrupt:
    try:
        sys.exit(0)
    except Exception as e:
        print("Erro:", e)