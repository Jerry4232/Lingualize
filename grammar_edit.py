"""
grammar_edit.py

send converted text(string) to sampling and receive json formatted edit
"""

import requests
from pprint import pprint

# these are public testing APIs, safe to push to github.

class SamplingClient:
    def __init__(self):
        self._key = 'ERL7C407NE4919NP3VWGAP9C5EFZTEUH'
        self._url = 'https://api.sapling.ai/api/v1/edits'

        self.edit_result: list[dict] = list()
        self.text_result: str = ""

    def format_data(self, text, session_id):
        """

        :param key:
        :param text:
        :param session_id:
        :return: {
                'key': key,
                'text': 'Could you talk me about something about California?',
                'session_id': 'Test Document UUID',
                'advanced_edits': {
                    'advanced_edits': True,
                },
            }
        """
        json_data = {
            'key': self._key,
            'text': text,
            'session_id': session_id,
            'advanced_edits': {
                'advanced_edits': True,
            }
        }
        return json_data

    #ignore misspelling error, assume the text that transcribed by assemblyAI is spelling correct.
    #category of errors can be found in this document.
    #https://sapling.ai/docs/api/error-categories/

    def advanced_check(self, data):
        """

        :param data:
            example: {'key': 'A1ROO8U62ATB1KMYWUS9N51VMY0U40RG',
                'text': ('I have went to the store yesterday but forgot buying milk,
                it was a really tiring day and I dont think I will go there again so soon.',),
                'session_id': 'test session',
                'advanced_edits': {'advanced_edits': True}}

        :return: edits in json format if successful
            return None when request failed
        """

        try:
            response = requests.post(self._url, json=data)
            resp_json = response.json()
            if 200 <= response.status_code < 300:
                edits = resp_json['edits']
                # printing the edits made by sampling
                # pprint(edits)
                return edits
            else:
                print('Error: ', resp_json)
        except Exception as e:
            print('Error: ', e)


    def fix_grammar_error(self, text: str, edits) -> str:
        """

        :param text: the string that we want to revise
        :param edits: the json data receive from
        :return: new string with replaced text
        """
        text = str(text)
        edits = sorted(edits, key=lambda e: (e['sentence_start'] + e['start']), reverse=True)
        for edit in edits:
            start = edit['sentence_start'] + edit['start']
            end = edit['sentence_start'] + edit['end']
            if start > len(text) or end > len(text):
                print(f'Edit start:{start}/end:{end} outside of bounds of text:{text}')
                continue
            text = text[: start] + edit['replacement'] + text[end:]
        return text


    def grammar_check(self, text: str):
        """
        :param text: the string that we want to revise
        :return: edits in json format if successful
            new_text in string format
        """
        data = self.format_data(text, "test session")
        edits = self.advanced_check(data)
        #
        new_text = ""
        if edits:
            new_text = self.fix_grammar_error(text, edits)

        # temporary stored in attributes
        self.edit_result = edits
        self.text_result = new_text

        return edits, new_text

    def get_result(self) -> tuple[list[dict], str]:
        """
        After calling grammar check, the returned value will be temporarily stored here
            these data will be deleted after getting them.
        :return: edits in json format if successful
            new_text in string format
        """
        edit, text = self.edit_result, self.text_result
        self.edit_result = []
        self.text_result = ""
        return edit, text

if __name__ == "__main__":
    text: str = "I have went to the store yesterday but forgot buying milk, "\
            "it was a really tiring day and I dont think I will go there again so soon."
    sc = SamplingClient()
    edit, new_text = sc.grammar_check(text)
    print(f"edit: {edit}")
    print(f"new_text: {new_text}")
