import azure.cognitiveservices.speech as speechsdk
import json

# print to interface for testing purpose, finally return a json file. 
# please reference to https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment?pivots=programming-language-python



def pronunciation_assessment_configured_with_json(filename):
    """Performs pronunciation assessment asynchronously with input from an audio file.
        See more information at https://aka.ms/csspeech/pa"""

    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    # Note: The sample is for en-US language.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=filename)

    reference_text = "Hello, could you give me some feedback?"
    # Create pronunciation assessment config with json string (JSON format is not recommended)
    enable_miscue, enable_prosody = True, True
    config_json = {
        "GradingSystem": "HundredMark",
        "Granularity": "Phoneme",
        "Dimension": "Comprehensive",
        "ScenarioId": "",  # "" is the default scenario or ask product team for a customized one
        "EnableMiscue": enable_miscue,
        "EnableProsodyAssessment": enable_prosody,
        "NBestPhonemeCount": 0,  # > 0 to enable "spoken phoneme" mode, 0 to disable
    }
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(json_string=json.dumps(config_json))
    pronunciation_config.reference_text = reference_text

    # Create a speech recognizer using a file as audio input.
    language = 'en-US'
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=language, audio_config=audio_config)
    # (Optional) get the session ID
    speech_recognizer.session_started.connect(lambda evt: print(f"SESSION ID: {evt.session_id}"))
    # Apply pronunciation assessment config to speech recognizer
    pronunciation_config.apply_to(speech_recognizer)

    result = speech_recognizer.recognize_once_async().get()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print('pronunciation assessment for: {}'.format(result.text))
        pronunciation_result = json.loads(result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult))
        print('assessment results:\n{}'.format(json.dumps(pronunciation_result, indent=4)))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            


filename = "user_input.wav"
pronunciation_assessment_configured_with_json(filename)