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
PRE_AUDIO = 0.5  # Seconds to prepend

def mainTask(threshold=SILENCE_MAX_VOLUME):
    p = pyaudio.PyAudio()
    #---Create pyaudio stream
    stream = p.open(format=FORMAT,
                    channels=THECHANNELS,
                    rate=SAMPLERATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Listening mic. ")
    finalAudio = []
    curChunk = ''  # current chunk  of audio data
    slid_win = deque(maxlen=math.floor(SILENCE_STOP_TIME * (RATE/CHUNK)))
    #---Prepend audio from 0.5 seconds before noise was detected
    pre_audio = deque(maxlen=math.floor(PRE_AUDIO * (RATE/CHUNK)))
    started = False # used to control whether or not user has started the recording
    response = []

    while (True):
        curChunk = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        #print slid_win[-1]
        if(sum([x > SILENCE_MAX_VOLUME for x in slid_win]) > 0):
            if(not started):
                print ("Recording beginning...")
                started = True
            finalAudio.append(curChunk)
        elif (started is True):
            stream.stop_stream()
            print ("Finished recording.")
            #(NEED DEFINITION) filename = save_speech(list(pre_audio) + finalAudio, p)
            #(NEED DEFINITION) p = stt_google_wav(filename)
            if p == "exit":
                break
            # Remove temp file. Comment line to review.
            os.remove(filename)
            # Reset all
            started = False
            slid_win = deque(maxlen=math.floor(SILENCE_STOP_TIME * (RATE/CHUNK)))
            pre_audio = deque(maxlen=math.floor(0.5 * (RATE/CHUNK)))
            finalAudio = []
            # (NEED DEFINITION) stream.start_stream()
            print ("Listening ...")
        else:
            pre_audio.append(curChunk)

    print ("exiting")
    p.terminate()
    return
