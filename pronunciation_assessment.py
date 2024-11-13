import azure.cognitiveservices.speech as speechsdk
import json

# print to interface for testing purpose, finally return a json file. 
# please reference to https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment?pivots=programming-language-python

def pronunciation_assessment_continuous_from_file():
    """Performs continuous pronunciation assessment asynchronously with input from an audio file.
        See more information at https://aka.ms/csspeech/pa"""

    import difflib
    import json

    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    # Note: The sample is for en-US language.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=zhcnlongfilename)

    with open("user_input.wav", "r", encoding="utf-8") as t:
        reference_text = t.readline()
    # Create pronunciation assessment config, set grading system, granularity and if enable miscue based on your requirement.
    enable_miscue = True
    enable_prosody_assessment = True
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(
        reference_text=reference_text,
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
        enable_miscue=enable_miscue)
    if enable_prosody_assessment:
        pronunciation_config.enable_prosody_assessment()

    # Creates a speech recognizer using a file as audio input.
    language = 'zh-CN'
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=language, audio_config=audio_config)
    # Apply pronunciation assessment config to speech recognizer
    pronunciation_config.apply_to(speech_recognizer)

    done = False
    recognized_words = []
    prosody_scores = []
    fluency_scores = []
    durations = []
    startOffset = 0
    endOffset = 0

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    def recognized(evt: speechsdk.SpeechRecognitionEventArgs):
        print("pronunciation assessment for: {}".format(evt.result.text))
        pronunciation_result = speechsdk.PronunciationAssessmentResult(evt.result)
        print("    Accuracy score: {}, prosody score: {}, pronunciation score: {}, completeness score : {}, fluency score: {}".format(
            pronunciation_result.accuracy_score, pronunciation_result.prosody_score, pronunciation_result.pronunciation_score,
            pronunciation_result.completeness_score, pronunciation_result.fluency_score
        ))
        nonlocal recognized_words, prosody_scores, fluency_scores, durations, startOffset, endOffset
        recognized_words += pronunciation_result.words
        fluency_scores.append(pronunciation_result.fluency_score)
        if pronunciation_result.prosody_score is not None:
            prosody_scores.append(pronunciation_result.prosody_score)
        json_result = evt.result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
        jo = json.loads(json_result)
        nb = jo["NBest"][0]
        durations.extend([int(w["Duration"]) + 100000 for w in nb["Words"]])
        if startOffset == 0:
            startOffset = nb["Words"][0]["Offset"]
        endOffset = nb["Words"][-1]["Offset"] + nb["Words"][-1]["Duration"] + 100000

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognized.connect(recognized)
    # (Optional) get the session ID
    speech_recognizer.session_started.connect(lambda evt: print(f"SESSION ID: {evt.session_id}"))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # Stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous pronunciation assessment
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()

    # We need to convert the reference text to lower case, and split to words, then remove the punctuations.
    if language == 'zh-CN':
        # Split words for Chinese using the reference text and any short wave file
        reference_words = get_reference_words(zhcnfilename, reference_text, language)
    else:
        reference_words = [w.strip(string.punctuation) for w in reference_text.lower().split()]

    # For continuous pronunciation assessment mode, the service won't return the words with `Insertion` or `Omission`
    # even if miscue is enabled.
    # We need to compare with the reference text after received all recognized words to get these error words.
    if enable_miscue:
        diff = difflib.SequenceMatcher(None, reference_words, [x.word.lower() for x in recognized_words])
        final_words = []
        for tag, i1, i2, j1, j2 in diff.get_opcodes():
            if tag in ['insert', 'replace']:
                for word in recognized_words[j1:j2]:
                    word._error_type = 'Insertion'
                    final_words.append(word)
            if tag in ['delete', 'replace']:
                for word_text in reference_words[i1:i2]:
                    word = speechsdk.PronunciationAssessmentWordResult({
                        'Word': word_text,
                        'PronunciationAssessment': {
                            'ErrorType': 'Omission',
                        }
                    })
                    final_words.append(word)
            if tag == 'equal':
                final_words += recognized_words[j1:j2]
    else:
        final_words = recognized_words

    durations_sum = sum([d for w, d in zip(recognized_words, durations) if w.error_type == "None"])

    # We can calculate whole accuracy by averaging
    final_accuracy_scores = []
    for word in final_words:
        if word.error_type == 'Insertion':
            continue
        else:
            final_accuracy_scores.append(word.accuracy_score)
    accuracy_score = sum(final_accuracy_scores) / len(final_accuracy_scores)
    # Re-calculate the prosody score by averaging
    if len(prosody_scores) == 0:
        prosody_score = float("nan")
    else:
        prosody_score = sum(prosody_scores) / len(prosody_scores)
    # Re-calculate fluency score
    fluency_score = 0
    if startOffset > 0:
        fluency_score = durations_sum / (endOffset - startOffset) * 100
    # Calculate whole completeness score
    handled_final_words = [w.word for w in final_words if w.error_type != "Insertion"]
    completeness_score = len([w for w in final_words if w.error_type == "None"]) / len(handled_final_words) * 100
    completeness_score = completeness_score if completeness_score <= 100 else 100
    sorted_scores = sorted([accuracy_score, prosody_score, completeness_score, fluency_score])
    pronunciation_score = sorted_scores[0] * 0.4 + sorted_scores[1] * 0.2 + sorted_scores[2] * 0.2 + sorted_scores[3] * 0.2

    print('    Paragraph pronunciation score: {:.2f}, accuracy score: {:.2f}, prosody score: {:.2f}, completeness score: {:.2f}, fluency score: {:.2f}'.format(
        pronunciation_score, accuracy_score, prosody_score, completeness_score, fluency_score
    ))

    for idx, word in enumerate(final_words):
        print('    {}: word: {}\taccuracy score: {}\terror type: {};'.format(
            idx + 1, word.word, word.accuracy_score, word.error_type
        ))
