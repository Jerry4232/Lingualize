import assemblyai as aai


class AssemblyClient:
    def __init__(self, ASSEMBLY_API_KEY, transcript_queue):
        aai.settings.api_key = ASSEMBLY_API_KEY
        self.transcript_queue = transcript_queue

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



