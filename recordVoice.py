import pyaudio # (MUST INSTALL FIRST)
import wave

form_1 = pyaudio.paInt16 # 16-bit resolution
theChans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 10 # seconds to record (CHANGE THIS TO STOP RECORDING AFTER 2-3 SECONDS OF SILENCE)
dev_index = 2 # device index found by p.get_device_info_by_index(ii) (THIS MAY CHANGE DEPENDING ON THE PI)
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


# ------------------------------------------------------------------------------------------

#ATTEMPT AT USING SILENCE TO STOP RECORDING RATHER THAN PREDEFINING A TIME, NOT FINISHED

SILENCE_MAX_VOLUME = 1500  # The sound intensity that defines silence
SILENCE_STOP_TIME = 3  # Silence limit in seconds to stop the recording

def mainTask(threshold=SILENCE_MAX_VOLUME):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print ("* Listening mic. ")
    audio2send = []
    cur_data = ''  # current chunk  of audio data
    rel = RATE/CHUNK
    slid_win = deque(maxlen=math.floor(SILENCE_STOP_TIME * rel))
    #Prepend audio from 0.5 seconds before noise was detected
    prev_audio = deque(maxlen=math.floor(PREV_AUDIO * rel))
    started = False # used to control whether or not user has started the recording
    response = []

    while (True):
        cur_data = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        #print slid_win[-1]
        if(sum([x > SILENCE_MAX_VOLUME for x in slid_win]) > 0):
            if(not started):
                print ("Recording beginning...")
                started = True
            audio2send.append(cur_data)
        elif (started is True):
            stream.stop_stream()
            print ("Finished recording.")
            #(NEED DEFINITION) filename = save_speech(list(prev_audio) + audio2send, p)
            #(NEED DEFINITION) p = stt_google_wav(filename)
            if p == "exit":
                break
            # Remove temp file. Comment line to review.
            os.remove(filename)
            # Reset all
            started = False
            slid_win = deque(maxlen=math.floor(SILENCE_STOP_TIME * rel))
            prev_audio = deque(maxlen=math.floor(0.5 * rel))
            audio2send = []
            # (NEED DEFINITION) stream.start_stream()
            print ("Listening ...")
        else:
            prev_audio.append(cur_data)

    print ("exiting")
    p.terminate()
    return
