import sounddevice as sd
import numpy as np
import pydirectinput
import sys
import time

##tabela de frequências do Fernando Iazzetta https://iazzetta.eca.usp.br/tutor/acustica/introducao/tabela1.html
##primeiro lá da flauta -> 440Hz

fs = 44100 # frequência de amostragem
duration = 0.4  # segundos
blocksize = 4096

direction = ''

##print(sd.query_devices()) ##ver microfones
##sd.default.device = 1, 1     ##escolher microfones

##def recording():
    ##try:
        ##myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        ##sd.wait()
        ##musicNote = fourier(myrecording)
        ##print(musicNote)
        ##pressKey(musicNote)
        ##return 

    ##except Exception as e:
        ##print("Erro na função recording:", e)

def pressKey(frequency):
    global direction
    try:
        if 256 < frequency < 266:
            pydirectinput.keyUp('down')
            return
        elif 288< frequency < 298:
            pydirectinput.keyDown('down')
            return
        elif 324 < frequency < 334:
            if direction == 'left':
                pydirectinput.keyUp('left')
                pydirectinput.press('down')
                pydirectinput.keyDown('left')
                return
            if direction == 'right':
                pydirectinput.keyUp('right')
                pydirectinput.press('down')
                pydirectinput.keyDown('right')
            else:
                pydirectinput.press('down')
        elif 339 < frequency < 359:
            pydirectinput.keyUp('left')
            direction = ''
            return
        elif 381 < frequency < 401:
            pydirectinput.keyDown('left')
            direction = 'left'
            return
        elif 405 < frequency < 425:
            pydirectinput.press('left')
            return
        elif 430 < frequency < 450: 
            pydirectinput.keyDown('right')
            direction = 'right'
            return
        elif 483 < frequency < 503: 
            pydirectinput.keyUp('right')
            direction = ''
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
        window = np.hanning(N) #window pra evitar vazamento espectral
        mag = np.abs(np.fft.fft(recording.flatten() * window))[:N//2] #magnitudes das transformadas de fourier

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
    def callback(indata, frames, time, status):
        audio = indata[:, 0]

        volume = np.sqrt(np.mean(audio**2))
        if volume < 0.01:
            return  #se o som for pouco volumoso, não processa
        
        musicNote = fourier(audio)
        print(musicNote)
        pressKey(musicNote)

    with sd.InputStream(
        samplerate=fs,
        channels=1,
        blocksize=blocksize,
        callback=callback
    ):
        while True:
            time.sleep(0.1)
            pass

except KeyboardInterrupt:
    try:
        sys.exit(0)
    except Exception as e:
        print("Erro:", e)