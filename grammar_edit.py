import requests
from pprint import pprint

# these are public testing APIs, safe to push to github.
key = 'ERL7C407NE4919NP3VWGAP9C5EFZTEUH'
url = 'https://api.sapling.ai/api/v1/edits'



def format_data(key, text, session_id):
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
        'key': key,
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

def advanced_check(data):
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
        response = requests.post(url, json=data)
        resp_json = response.json()
        if 200 <= response.status_code < 300:
            edits = resp_json['edits']
            pprint(edits)
            return edits
        else:
            print('Error: ', resp_json)
    except Exception as e:
        print('Error: ', e)


def fix_grammar_error(text, edits):
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


def grammar_check(text):
    data = format_data(key, text, "test session")
    edits = advanced_check(data)
    if edits:
        new_text = fix_grammar_error(text, edits)
    return edits, new_text

if __name__ == "__main__":
    text: str = "I have went to the store yesterday but forgot buying milk, "\
            "it was a really tiring day and I dont think I will go there again so soon."

    data = format_data(key, text, "test session")
    edits = advanced_check(data)
    if edits:
        new_text = fix_grammar_error(text, edits)
        print(new_text)
    else:
        print('Error in requesting edits')
