# ------------------------------------------------------------------------------------------

#ATTEMPT AT USING SILENCE TO STOP RECORDING RATHER THAN PREDEFINING A TIME, NOT FINISHED

import wiringpi
import pyaudio
import wave
import audioop
from collections import deque
import os
import time
import math

SILENCE_MAX_VOLUME = 1500  # The sound intensity that defines silence
SILENCE_STOP_TIME = 3  # Silence limit in seconds to stop the recording
client = speech.Client()
LANG_CODE = 'en-US'
CHUNK = 1024  # Chunks of bytes to read each time from mic
FORMAT = pyaudio.paInt16
THECHANNELS = 1
SAMPLERATE = 16000
PREPEND_AUDIO = 0.5  # Seconds to prepend

def mainTask(threshold=SILENCE_MAX_VOLUME):
    audio = pyaudio.PyAudio()
    #---Create pyaudio stream
    stream = audio.open(format=FORMAT,
                    channels=THECHANNELS,
                    rate=SAMPLERATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Listening mic. ")
    finAudio = []
    curChunk = ''  # current chunk  of audio data
    silenceDeq = deque(maxlen=math.floor(SILENCE_STOP_TIME * (RATE/CHUNK)))
    #---Prepend audio from 0.5 seconds before noise was detected
    pre_audio = deque(maxlen=math.floor(PREPEND_AUDIO * (RATE/CHUNK)))
    began = False # used to control whether or not user has started the recording
    response = [] #(WHY NEEDED?)

    while (True):
        curChunk = stream.read(CHUNK)
        silenceDeq.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        #---Print silenceDeq[-1]
        if(sum([x > SILENCE_MAX_VOLUME for x in silenceDeq]) > 0):
            if(not began):
                print ("Recording beginning...")
                began = True
            finAudio.append(curChunk)
        elif (began is True):
            stream.stop_stream()
            print ("Finished recording.")
            filename = saveFile(list(pre_audio) + finAudio, p)
            #(NEED DEFINITION) p = stt_google_wav(filename)
            if p == "exit":
                break
            #---Remove temp file
            os.remove(filename)
            #---Reset all
            began = False
            silenceDeq = deque(maxlen=math.floor(SILENCE_STOP_TIME * (RATE/CHUNK)))
            pre_audio = deque(maxlen=math.floor(0.5 * (RATE/CHUNK)))
            finAudio = []
            #(NEED DEFINITION) stream.start_stream()
            print ("Listening ...")
        else:
            pre_audio.append(curChunk)

    print ("exiting")
    p.terminate()
    return

def saveFile(data, audio):
    filename = 'output_'+str(int(time.time()))
    #---Write data to WAV file
    data = b''.join(data)
    wf = wave.open(filename + '.wav', 'wb')
    wf.setnchannels(THECHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(SAMPLERATE)  # TODO make this value a function parameter?
    wf.writeframes(data)
    wf.close()
    return filename + '.wav'
