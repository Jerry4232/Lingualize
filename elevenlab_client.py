import requests  # Used for making HTTP requests
from io import BytesIO  # For handling audio in memory
from pydub import AudioSegment  # For handling audio playback
from pydub.playback import play  # For playing the audio

class ElevenlabClient:
    def __init__(self,ELEVENLABS_API_KEY):
        self.XI_API_KEY = ELEVENLABS_API_KEY

    def voice_generate(self, chunk_size: int, voice_id: str, text: str) -> None:
        """
        Converts text to speech using ElevenLabs' Text-to-Speech (TTS) API and plays the audio.

        Args:
            chunk_size (int): Size of data chunks for streaming.
            voice_id (str): ID of the voice model to use from ElevenLabs.
            text (str): Text content to be converted into speech.

        Returns:
            None
        """
        # Construct the URL for the Text-to-Speech API request
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

        # Set up headers for the API request, including the API key for authentication
        headers = {
            "Accept": "application/json",
            "xi-api-key": self.XI_API_KEY
        }

        # Define the data payload for the API request, including voice settings
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }

        # Send the POST request to ElevenLabs TTS API with streaming enabled
        response = requests.post(tts_url, headers = headers, json = data, stream = True)

        if response.ok:
            # Create an in-memory byte buffer to hold the audio stream
            audio_stream = BytesIO()

            # Stream and save the audio data in chunks to the buffer
            for chunk in response.iter_content(chunk_size = chunk_size):
                audio_stream.write(chunk)

            # Reset buffer to the beginning
            audio_stream.seek(0)

            # Load the audio stream as an AudioSegment for playback
            audio = AudioSegment.from_file(audio_stream, format = "mp3")

            # Play the generated audio
            play(audio)
            # print("Audio played successfully.")
        else:
            # Print the error message if the request was not successful
            print(f"Error generating audio: {response.text}")
