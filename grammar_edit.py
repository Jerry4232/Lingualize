import requests
from pprint import pprint

# these are public testing APIs, safe to push to github.
key = 'A1ROO8U62ATB1KMYWUS9N51VMY0U40RG'
url = 'https://api.sapling.ai/api/v1/edits'

data = {
    'key': key,
    'text': 'Could you tell me about something about California?',
    'session_id': 'Test Document UUID',
    'advanced_edits': {
        'advanced_edits': True,
    },
}

def format_data(key, text, session_id):
    data = {
        'key': key,
        'text': text,
        'session_id': session_id,
        'advanced_edits': {
            'advanced_edits': True,
        },
    }
    return data

#ignore misspelling error, assume the text that transcribed by assemblyAI is spelling correct.
#category of errors can be found in this document.
#https://sapling.ai/docs/api/error-categories/

def advanced_check(data):
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