from openai import OpenAI
import textwrap


class OpenaiClient:
    def __init__(self, OpenAI_API_KEY):
        self.client = OpenAI(api_key = OpenAI_API_KEY)
        self.text_result = "OpenAI"

    def generate_and_play_response(self, transcript_result):
        """
        Generates a response using GPT-3.5 based on the provided transcript and plays it using ElevenLabs TTS.

        Args:
            transcript_result (str): The user's transcribed speech.

        Returns:
            None
        """

        # print("GPT Connected")
        reply = self.client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system",
                 "content": "You are a friendly and knowledgeable coffee shop employee.Answer questions warmly and concisely within 40 characters, providing customers with information on menu items, drink customizations, recommendations, and store policies. Use a welcoming tone and assist as if speaking directly to a customer in the shop."},
                {"role": "user", "content": transcript_result}
            ]
        )
        text = reply.choices[0].message.content

        # wrapped_text = textwrap.fill(text, width = 100)
        # print(wrapped_text)
        self.text_result = text

        return text

    def get_text_result(self):
        result = self.text_result
        self.text_result = ""
        return result
