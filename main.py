import itertools
import threading
import time
from queue import Queue

# Import keys securely
from config import OpenAI_API_KEY, ELEVENLABS_API_KEY
from elevenlab_client import ElevenlabClient
from openai_client import OpenaiClient
from grammar_edit import SamplingClient
from emotion_detect import record_audio, transcribe_audio, format_emotion_data
from pronunciation_assessment import SpeechSDKClient

elevenlabs_voice_id = "9BWtsMINqrJLrRacOk9x"
audio_filename = "user_input.wav"
reference_text = "Hello, could you give me some feedback?"
spinner = itertools.cycle(['Loading.', 'Loading..', 'Loading...', 'Loading....',
                    'Loading.....', 'Loading......', 'Loading.......', 'Loading........'])

def main():
    """
    Manages the full conversation loop, including transcription, response generation, and audio playback.

    Establishes a connection to the transcriber, streams audio from the microphone, and processes
    each transcription in real-time. If an error or interruption occurs, it closes the connection.

    Returns:
        None
    """

    # Set API keys
    transcript_queue = Queue()
    open_ai_tool = OpenaiClient(OpenAI_API_KEY)
    elevenlabs_tool = ElevenlabClient(ELEVENLABS_API_KEY)
    sampling_tool = SamplingClient()
    sdk_tool = SpeechSDKClient()

    try:
        record_audio(audio_filename, timeout = 1, silence_threshold = 800)
        transcript_result = transcribe_audio(audio_filename)
        print(f"User: {transcript_result}")
        print()
        print(f"User Emotion: {format_emotion_data(transcript_result)}")
        print()
    except KeyboardInterrupt:
        print("Conversation ended by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

    def display_spinner():
        """A thread that displays a spinner animation until stopped."""
        try:
            while open_ai_tool.text_result:
                print(f"\r{next(spinner)}", end = "", flush = True)
                time.sleep(1)  # Adjust speed of the spinner
        finally:
            print("                    ", end = "\n", flush = True)
            print("Finished.")
    loading = threading.Thread(
        target = display_spinner
    )
    open_ai_thread = threading.Thread(
        target = open_ai_tool.generate_and_play_response, args = (transcript_result,))
    sdk_thread = threading.Thread(
        target=sdk_tool.get_accuracy_score, args = (audio_filename, reference_text))
    sampling_thread = threading.Thread(
        target = sampling_tool.grammar_check, args = (transcript_result,))

    loading.start()
    open_ai_thread.start()
    sdk_thread.start()
    sampling_thread.start()

    open_ai_thread.join()  # Waits for open_ai_thread to finish
    sdk_thread.join()
    sampling_thread.join()  # Waits for sampling_thread to finish

    # get the result and empty the class attribute - respond from gpt
    text = open_ai_tool.get_text_result()
    edit, new_text = sampling_tool.get_result()
    pronunciation = sdk_tool.get_result()

    # Convert the response to audio
    elevenlabs_tool.voice_generate(1024, elevenlabs_voice_id, text)
    if text:
        print("AI:", text)
        print()
    if new_text:
        # Sampling
        print("Suggested revision:", new_text)
    if pronunciation:
        print("Pronunciation rating:", pronunciation)


# Run the conversation loop
if __name__ == '__main__':
    main()
