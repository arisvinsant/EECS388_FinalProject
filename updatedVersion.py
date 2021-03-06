#-----------------------------------Recording section---------------------------------------

import pyaudio
import wave
import io
import os

form_1 = pyaudio.paInt16 # 16-bit resolution
theChans = 1 # 1 channel
samp_rate = 48000 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 10 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii) 
#^ this will change, we need to get this before we start
output_filename = 'teamTwelveAudio.wav' # name of .wav file (ARBITRARY)

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = theChans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
print("Recording...")
frames = []

# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk)
    frames.append(data)

print("Ended recording.")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(output_filename,'wb')
wavefile.setnchannels(theChans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close() #(OUTPUT FILE, USE THIS TO PASS INTO THE API FOR TRANSLATION)

#--------------------------------Transcribe section-------------------------------------------

import speech_recognition as sr

r = sr.Recognizer()

audio = 'teamTwelveAudio.wav'

with sr.AudioFile(audio) as source:
    audio = r.record(source)
    print ('Done!')
    
try:
    text = r.recognize_google(audio)
    print (text)
    
except Exception as e:
    print (e)
