#assembly_client.py
"""_summary_
        This module provides real-time audio transcription capabilities using the AssemblyAI API. It defines the 
AssemblyClient class, which initializes and manages a real-time transcriber instance, enabling continuous 
conversion of spoken audio into text. Designed with callbacks for handling data and errors, this module 
offers an efficient setup for real-time transcription applications.
"""
from queue import Empty
import assemblyai as aai


class AssemblyClient:
    def __init__(self, ASSEMBLY_API_KEY, transcript_queue):
        aai.settings.api_key = ASSEMBLY_API_KEY
        self.transcript_queue = transcript_queue
        self.transcribed_text = ""
       

    def get_transcriber(self):
        return aai.RealtimeTranscriber(
            on_data = self.on_data,
            on_error = AssemblyClient.on_error,
            sample_rate = 44_100,
        )

    @staticmethod
    def on_error(error: aai.RealtimeError):
        """
        Callback function to handle errors in the transcription process.

        Args:
            error (aai.RealtimeError): Error object containing information about the encountered error.

        Returns:
            None
        """
        print("An error occurred:", error)

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
            self.transcribed_text = transcript.text


    def get_transcript(self, audio, transcriber):
        transcriber.stream(audio)
        all_text = []
        while True:
            try:
                item = self.transcript_queue.get(timeout=1)
                all_text.append(item)
                self.transcript_queue.task_done()
            except Empty:
                break
        transcript_result = " ".join(all_text)
        return transcript_result

