from emotion_detect import audio_get_emotion_and_text
from pronunciation_assessment import pronunciation_assessment_configured_with_json
from openai_client import OpenaiClient
from grammar_edit import grammar_check
from elevenlab_client import ElevenlabClient

from config import OpenAI_API_KEY, ELEVENLABS_API_KEY
open_ai_tool = OpenaiClient(OpenAI_API_KEY)
elevenlabs_tool = ElevenlabClient(ELEVENLABS_API_KEY)
elevenlabs_voice_id = "9BWtsMINqrJLrRacOk9x"

#Step1: analyze emotion and transcribe from audio to text
emotion_and_text, audio_file_name = audio_get_emotion_and_text()
transcript_result = emotion_and_text.get("text")
print("user: ", transcript_result)

#missing GPT preprompt

#Step2: gpt generate response
GPT_response = open_ai_tool.generate_and_play_response(transcript_result)
print("GPT: ", GPT_response)

#Step3: elevenlabs generate voices
elevenlabs_tool.voice_generate(1024, elevenlabs_voice_id, GPT_response)
pronunciation_score = pronunciation_assessment_configured_with_json(audio_file_name,"")
print("Here is your pronunciation result: ", pronunciation_score)

#Step3: analyze grammar error and return revised text
grammar_errors, revised_text = grammar_check(transcript_result)
print("You have these grammar errors", grammar_errors)
print("Here is your revised text: ",revised_text)


