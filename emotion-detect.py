import os
import pyaudio
import wave
import time
import audioop
import json
from ibm_watson import SpeechToTextV1, NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Configuration for IBM Speech-to-Text
SPEECH_TO_TEXT_API_KEY = 'AD38snU5-7C_ecxmyGd-InQyLw2TbMhwYrOKbS5Dl7XL'
SPEECH_TO_TEXT_URL = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/d2f8fdf2-ee5f-4c30-bd44-ce5545c69ca5'
speech_authenticator = IAMAuthenticator(SPEECH_TO_TEXT_API_KEY)
speech_to_text = SpeechToTextV1(authenticator=speech_authenticator)
speech_to_text.set_service_url(SPEECH_TO_TEXT_URL)

# Configuration for IBM Natural Language Understanding (NLU)
NLU_API_KEY = 'NjQEWTSvNxR6lb40MI-oxDQdGt_42jdtIhJPA2a_EtUB'
NLU_URL = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/924bda34-966f-4151-acc9-beb2ab34ab02'
nlu_authenticator = IAMAuthenticator(NLU_API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=nlu_authenticator
)
nlu.set_service_url(NLU_URL)

import pyaudio
import wave
import time
import audioop

def record_audio(filename, timeout=1, silence_threshold=800, max_silence_duration=6):
    """Record audio until silence is detected or max silence duration is reached"""
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    rate = 16000

    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    
    print("Recording...")
    frames = []
    last_sound_time = time.time()
    total_silence_time = 0  # Track cumulative silence duration

    while True:
        data = stream.read(chunk)
        frames.append(data)
        
        # Detect silence by calculating the RMS (Root Mean Square) of the audio chunk
        rms = audioop.rms(data, 2)
        
        if rms > silence_threshold:
            # Sound detected, reset silence tracking variables
            last_sound_time = time.time()
            total_silence_time = 0  # Reset cumulative silence time when sound is detected
        else:
            # Accumulate total silence time
            total_silence_time = time.time() - last_sound_time

        # Stop recording if silence exceeds either timeout or max_silence_duration
        if total_silence_time >= max_silence_duration or total_silence_time > timeout:
            break

    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))


def transcribe_audio(filename):
    """Convert recorded audio to text"""
    with open(filename, 'rb') as audio_file:
        result = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/wav'
        ).get_result()
    
    if result['results']:
        transcript = result['results'][0]['alternatives'][0]['transcript']
        return transcript
    else:
        return None

def analyze_emotion(text):
    """Analyze the emotions in the text and return results in JSON"""
    response = nlu.analyze(
        text=text,
        features=Features(emotion=EmotionOptions())
    ).get_result()
    emotions = response['emotion']['document']['emotion']
    result = {
        "text": text,
        "emotions": {
            "anger": round(emotions['anger'], 2),
            "joy": round(emotions['joy'], 2),
            "sadness": round(emotions['sadness'], 2),
            "disgust": round(emotions['disgust'], 2),
            "fear": round(emotions['fear'], 2)
        }
    }
    return json.dumps(result, indent=4)

def testing_main():
    """This method is for testing only. """
    # Step 1: Record audio until silence is detected
    audio_filename = "user_input.wav"
    record_audio(audio_filename, timeout=1, silence_threshold=800)

    # Step 2: Convert audio to text
    text = transcribe_audio(audio_filename)
    
    if text:
        print(f"Transcribed text: {text}")
        
        # Step 3: Check the word count of the text
        words = text.split()
        if len(words) <= 4:
            result = {
                "error": "The sentence is too short for analysis",
                "text": text
            }
            print(json.dumps(result, indent=4))
        else:
            # Perform emotion analysis and output as JSON
            emotion_result = analyze_emotion(text)
            print(emotion_result)
    else:
        result = {
            "error": "No valid text recognized"
        }
        print(json.dumps(result, indent=4))



def main():
    """this method will interact with front-end, sending the transcribe text and emotion analysis result."""
    # Step 1: Record audio until silence is detected
    audio_filename = "user_input.wav"
    record_audio(audio_filename, timeout=1, silence_threshold=800)

    # Step 2: Convert audio to text
    text = transcribe_audio(audio_filename)
    
    if text:
        # Step 3: Check the word count of the text
        words = text.split()
        if len(words) <= 4:
            result = {
                "error": "The sentence is too short for analysis",
                "text": text,
                "emotion": None
            }
        else:
            # Perform emotion analysis and ensure it’s a dictionary
            emotion_result = analyze_emotion(text)
            
            # Convert to a dictionary if it's a JSON string
            if isinstance(emotion_result, str):
                emotion_result = json.loads(emotion_result)
            
            result = {
                "text": text,
                "emotion": emotion_result
            }
    else:
        result = {
            "error": "No valid text recognized",
            "text": None,
            "emotion": None
        }
    
    # Return the result in JSON format
    return json.dumps(result, indent=4)


if __name__ == "__main__":
    a = main()
    print(a)
    