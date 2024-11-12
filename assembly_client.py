#assembly_client.py
"""_summary_
        This module provides real-time audio transcription capabilities using the AssemblyAI API. It defines the 
AssemblyClient class, which initializes and manages a real-time transcriber instance, enabling continuous 
conversion of spoken audio into text. Designed with callbacks for handling data and errors, this module 
offers an efficient setup for real-time transcription applications.
"""

import assemblyai as aai


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
    def __init__(self, ASSEMBLY_API_KEY, transcript_queue):
        aai.settings.api_key = ASSEMBLY_API_KEY
        self.transcript_queue = transcript_queue
        self.current_text = ""

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
            self.transcript_queue.put(transcript.text + '')
            print("User:", transcript.text, end = "\r\n")
            self.current_text = transcript.text

    def get_text(self):
        return self.current_text



