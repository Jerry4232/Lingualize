import azure.cognitiveservices.speech as speechsdk
# print to interface for testing purpose, finally return a json file. 
# please reference to https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment?pivots=programming-language-python

import azure.cognitiveservices.speech as speechsdk
import json

speech_key = "DWXaHr3TA4MzTup7z9URhzGB37zUmzxv3NMc2or9srwj7bLMeRwnJQQJ99AKAC4f1cMXJ3w3AAAYACOG3GPM"
service_region = "westus"

import azure.cognitiveservices.speech as speechsdk

import azure.cognitiveservices.speech as speechsdk
import threading

def pronunciation_and_grammar_assessment_with_custom_stream(mic_stream, speech_key, service_region):
    """Performs pronunciation and grammar assessment asynchronously with input from a universal microphone stream."""

    # Set up the speech configuration
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "3000")

    # Set up pronunciation assessment configuration
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
        enable_miscue=True
    )
    pronunciation_config.enable_prosody_assessment()  # Enable prosody (intonation) assessment
    # pronunciation_config.enable_content_assessment_with_topic(reference_text)  # Enable grammar assessment

    # Create a PushAudioInputStream and AudioConfig for Azure Speech SDK
    push_stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=push_stream)

    # Create a recognizer with the speech configuration and audio input stream
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    pronunciation_config.apply_to(recognizer)

    # Define a function to continuously push data from the microphone stream to Azure's PushAudioInputStream
    def push_audio_data():
        try:
            while True:
                data = mic_stream.read(1024)  # Read data from the universal mic stream
                if not data:
                    break
                push_stream.write(data)
        except Exception as e:
            print("Error reading microphone stream:", e)
        finally:
            push_stream.close()

    # Start the audio pushing in a separate thread
    audio_thread = threading.Thread(target=push_audio_data)
    audio_thread.start()

    # Start the assessment
    # print(f"Read out '{reference_text}' for pronunciation and grammar assessment...")
    result = recognizer.recognize_once()

    # Stop the audio thread
    audio_thread.join()

    # Check and handle the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")

        # Extract pronunciation assessment results
        pronunciation_result = speechsdk.PronunciationAssessmentResult(result)
        print("Pronunciation Assessment Results:")
        print(f"  Accuracy Score: {pronunciation_result.accuracy_score}")
        print(f"  Fluency Score: {pronunciation_result.fluency_score}")
        print(f"  Completeness Score: {pronunciation_result.completeness_score}")
        print(f"  Pronunciation Score: {pronunciation_result.pronunciation_score}")
        
        # Extract content assessment results for grammar, vocabulary, and topic scores
        content_result = pronunciation_result.content_assessment_result
        if content_result:
            print("Content (Grammar) Assessment Results:")
            print(f"  Grammar Score: {content_result.grammar_score}")
            print(f"  Vocabulary Score: {content_result.vocabulary_score}")
            print(f"  Topic Score: {content_result.topic_score}")

        # Display word-level pronunciation details
        print("Word-level details:")
        for idx, word in enumerate(pronunciation_result.words):
            print(f"  {idx + 1}: word: '{word.word}', accuracy score: {word.accuracy_score}, error type: {word.error_type}")

    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")


