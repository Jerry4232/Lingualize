from openai import OpenAI
import textwrap


class OpenaiClient:
    def __init__(self, OpenAI_API_KEY):
        self.client = OpenAI(api_key = OpenAI_API_KEY)

    def generate_and_play_response(self, transcript_result):
        """
        Generates a response using GPT-3.5 based on the provided transcript and plays it using ElevenLabs TTS.

        Args:
            transcript_result (str): The user's transcribed speech.

        Returns:
            None
        """

        print("GPT Connected")
        reply = self.client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system",
                 "content": "You are a highly skilled AI, answer questions concisely within 1000 characters."},
                {"role": "user", "content": transcript_result}
            ]
        )
        text = reply.choices[0].message.content

        wrapped_text = textwrap.fill(text, width = 100)
        print(wrapped_text)

        return text
