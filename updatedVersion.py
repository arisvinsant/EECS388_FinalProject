#-----------------------------------Recording section---------------------------------------

import pyaudio
import wave

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

def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        
transcribe_file(teamTwelveAudio.wav) #this may need to be changed
