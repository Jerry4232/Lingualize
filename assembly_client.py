#assembly_client.py
"""_summary_
        This module provides real-time audio transcription capabilities using the AssemblyAI API. It defines the 
AssemblyClient class, which initializes and manages a real-time transcriber instance, enabling continuous 
conversion of spoken audio into text. Designed with callbacks for handling data and errors, this module 
offers an efficient setup for real-time transcription applications.
"""
from operator import rshift
from queue import Queue, Empty

import assemblyai as aai
from assemblyai import RealtimeTranscriber
from config import ASSEMBLY_API_KEY


def on_error(error: aai.RealtimeError):
    """
    Callback function to handle errors in the transcription process.

    Args:
        error (aai.RealtimeError): Error object containing information about the encountered error.

    Returns:
        None
    """
    print("An error occurred:", error)


class AssemblyClient:
    def __init__(self):
        aai.settings.api_key = ASSEMBLY_API_KEY
        self.transcript_list = list()
        self.current_text = ""
        self.transcriber = self.get_transcriber()

    def get_transcriber(self):
        return aai.RealtimeTranscriber(
            on_data = self.on_data,
            on_error = on_error,
            sample_rate = 44_100,
        )


    def on_data(self, transcript: aai.RealtimeTranscript):
        """
        Callback function to handle incoming transcription data.

        Args:
            transcript (aai.RealtimeTranscript): Transcript data received from the transcriber.

        Returns:
            None
        """
        if not transcript.text:
            return
        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print("User:", transcript.text, end = "\r\n")
            self.transcript_list.append(transcript.text)

    def record_transcript_text(self):
        self.transcript_queue = Queue()
        try:
            self.transcriber.connect()
            print("Successfully Connected!")
            while True:
                try:
                    microphone_stream = aai.extras.MicrophoneStream()
                    print("Press Ctrl+C to stop recording.")
                    self.transcriber.stream(microphone_stream)
                    print("output get!")
                    break
                except Empty:
                    continue
        except KeyboardInterrupt:
            print("Conversation ended by user.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if isinstance(self.transcriber, RealtimeTranscriber):
                self.transcriber.close()
                # Combine all text items into a single string
                # print("Transcriber connection closed.")
            transcript_result = " ".join(self.transcript_list)
            return transcript_result


    def get_text(self):
        result = self.current_text
        self.current_text = ""
        self.transcript_list = list()
        return result


if __name__ == '__main__':
    ac = AssemblyClient()
    res = ac.record_transcript_text()
    print(f"You recorded: {res}")
