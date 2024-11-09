#API_multithreading.py
"""_summary_

"""
import pyaudio
import threading
import requests
# from grammar_edit import 
# from elevenlab_client import 

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# Initialize PyAudio
audio = pyaudio.PyAudio()


def microphone_stream():
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    try:
        while True:
            audio_chunk = stream.read(CHUNK)
            # Send audio_chunk to multiple APIs
            # threading.Thread(target=send_to_pronunciation_assessment, args=(audio_chunk,)).start()
            # threading.Thread(target=send_to_speech_recognition, args=(audio_chunk,)).start()
            # Add more threads for other APIs if needed
    except KeyboardInterrupt:
        print("Stopping microphone stream...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
