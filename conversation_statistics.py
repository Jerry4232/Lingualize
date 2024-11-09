#conversation_statistics.py
"""_summary_
        This module provides functionality to analyze sentence complexity using the Sapling AI API.
"""
import requests
from pprint import pprint

STATISTICS_URL = "https://api.sapling.ai/api/v1/statistics"

#more reference: https://sapling.ai/docs/api/statistics/

def sentence_complexity_analysis(URL, key, text, timeout=10):
    try:
        response = requests.post(
            URL,
            json={
                "key": key,
                "text": text,
            },
            timeout=timeout
        )
        pprint(response.json())
        return response
    except requests.exceptions.Timeout:
        print("The request timed out")
        return None

