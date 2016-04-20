"""Adapted from PyAudio wave player example"""

import pyaudio
import wave

def playWav(filename):
    CHUNK = 4096
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=False,output=True)

    data = wf.readframes(CHUNK)
    
    while(len(data) != 0):
        stream.write(data)
        data = wf.readframes(CHUNK)
        
    stream.stop_stream()
    stream.close()

    p.terminate()
