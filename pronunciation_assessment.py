import azure.cognitiveservices.speech as speechsdk
import json

# print to interface for testing purpose, finally return a json file. 
# please reference to https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment?pivots=programming-language-python

def pronunciation_assessment_from_microphone(speech_key, service_region):
    """Performs one-shot pronunciation assessment asynchronously with input from microphone.
        See more information at https://aka.ms/csspeech/pa"""

    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # The pronunciation assessment service has a longer default end silence timeout (5 seconds) than normal STT
    # as the pronunciation assessment is widely used in education scenario where kids have longer break in reading.
    # You can adjust the end silence timeout based on your real scenario.
    config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "3000")

    reference_text = ""
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(
        reference_text=reference_text,
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
        enable_miscue=True)
    pronunciation_config.enable_prosody_assessment()

    # Create a speech recognizer, also specify the speech language
    recognizer = speechsdk.SpeechRecognizer(speech_config=config, language="en-US")
    while True:
        # Receives reference text from console input.
        print('Enter reference text you want to assess, or enter empty text to exit.')
        print('> ', end='')

        try:
            reference_text = input()
        except EOFError:
            break

        if not reference_text:
            break

        pronunciation_config.reference_text = reference_text
        # (Optional) get the session ID
        recognizer.session_started.connect(lambda evt: print(f"SESSION ID: {evt.session_id}"))
        pronunciation_config.apply_to(recognizer)

        # Starts recognizing.
        print('Read out "{}" for pronunciation assessment ...'.format(reference_text))

        # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
        # shot evaluation.
        # For long-running multi-utterance pronunciation evaluation, use start_continuous_recognition() instead.
        result = recognizer.recognize_once_async().get()

        # Check the result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print('Recognized: {}'.format(result.text))
            print('  Pronunciation Assessment Result:')

            pronunciation_result = speechsdk.PronunciationAssessmentResult(result)
            print('    Accuracy score: {}, Prosody score: {}, Pronunciation score: {}, Completeness score : {}, FluencyScore: {}'.format(
                pronunciation_result.accuracy_score, pronunciation_result.prosody_score, pronunciation_result.pronunciation_score,
                pronunciation_result.completeness_score, pronunciation_result.fluency_score
            ))
            print('  Word-level details:')
            for idx, word in enumerate(pronunciation_result.words):
                print('    {}: word: {}, accuracy score: {}, error type: {};'.format(
                    idx + 1, word.word, word.accuracy_score, word.error_type
                ))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))