import assemblyai as aai
from queue import Queue, Empty
import pyaudio
import threading
from assembly_client import AssemblyClient
# Import keys securely
from config import OpenAI_API_KEY, ASSEMBLY_API_KEY, ELEVENLABS_API_KEY
from elevenlab_client import ElevenlabClient 
from openai_client import OpenaiClient
from pronunciation_assessment import pronunciation_and_grammar_assessment_with_custom_stream

from multithreading_api import run_tasks_concurrently

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000



import threading
from queue import Queue, Empty
import signal
import pyaudio

# Global flag to control the recording loop
stop_recording = False

# Function to handle Ctrl+C to stop recording
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
    audio = pyaudio.PyAudio()
    
    try:
        # Connect to the transcriber
        transcriber.connect()
        print("Successfully Connected!")
        
        # Open the audio stream for continuous recording
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print("Press Ctrl+C to stop recording.")
        
        while True:
            try:
                # Read a chunk of audio from the microphone
                audio_chunk = stream.read(CHUNK)
                
                # Start a thread to handle transcription asynchronously
                # result_queue = Queue()
                # thread1 = threading.Thread(target=assembly_tool.get_transcript, args=(audio_chunk, transcriber, result_queue))
                # thread1.start()
                # thread1.join()  # Wait for the thread to finish
                tasks = [
                     (assembly_tool.get_transcript, (audio_chunk, transcriber))
                ]
                results = run_tasks_concurrently(tasks)
                print(results[assembly_tool.get_transcript])
                
                # Get the transcription result from the queue
            except Empty:
                continue
            except Exception as e:
                print(f"An error occurred during transcription: {e}")
                break
        # if not result_queue.empty():
        #             transcript_result = result_queue.get()
                    
        #             # Generate a response using OpenAI
        #             text = open_ai_tool.generate_and_play_response(transcript_result)
                    
        #             # Convert the response text to audio and play it back
        #             elevenlabs_tool.voice_generate(1024, elevenlabs_voice_id, text)
        #             print("\nAI:", text)

    except KeyboardInterrupt:
        print("\nConversation ended by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup resources
        transcriber.close()
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Transcriber connection closed and audio stream terminated.")



# Run the conversation loop
if __name__ == '__main__':
    main()

 # threading.Thread(target=send_to_speech_recognition, args=(audio_chunk,)).start()
#                 tasks: list[tuple[FunctionType, tuple]] = [
#                     (assembly_tool.get_transcript, (audio_chunk,transcriber,)),
#                     (pronunciation_and_grammar_assessment_with_custom_stream
# , (audio_chunk,speech_key,service_region))
#                 ]
#                 print("output get!")
#                 results = run_tasks_concurrently(tasks)
#                 for result in results:
#                     print(result)