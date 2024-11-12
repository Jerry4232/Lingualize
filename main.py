import assemblyai as aai
from queue import Queue, Empty

from assembly_client import AssemblyClient
# Import keys securely
from config import OpenAI_API_KEY, ASSEMBLY_API_KEY, ELEVENLABS_API_KEY
from elevenlab_client import ElevenlabClient
from openai_client import OpenaiClient


elevenlabs_voice_id = "9BWtsMINqrJLrRacOk9x"

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
    assembly_tool = AssemblyClient(ASSEMBLY_API_KEY, transcript_queue)
    open_ai_tool = OpenaiClient(OpenAI_API_KEY)
    elevenlabs_tool = ElevenlabClient(ELEVENLABS_API_KEY)
    transcriber = assembly_tool.get_transcriber()

    try:
        transcriber.connect()
        print("Successfully Connected!")
        while True:
            try:
                microphone_stream = aai.extras.MicrophoneStream()
                print("Press Ctrl+C to stop recording.")
                transcriber.stream(microphone_stream)
                print("output get!")

                all_text = []
                while True:
                    try:
                        # Get recorded text from the queue with a timeout
                        item = transcript_queue.get(timeout=1)
                        all_text.append(item)  # Collect each item in the list
                        transcript_queue.task_done()
                    except Empty:
                        break

                # Combine all text items into a single string
                transcript_result = " ".join(all_text)
                text = open_ai_tool.generate_and_play_response(transcript_result)
                # Convert the response to audio
                elevenlabs_tool.voice_generate(1024, elevenlabs_voice_id, text)
                print("\nAI:", text)
            except Empty:
                continue

    except KeyboardInterrupt:
        print("Conversation ended by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        transcriber.close()
        print("Transcriber connection closed.")


# Run the conversation loop
if __name__ == '__main__':
    main()
