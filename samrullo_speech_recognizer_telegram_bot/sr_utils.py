import speech_recognition as sr
import pathlib


def recognize_speech_from_audio_file(
    recognizer: sr.Recognizer, audio_file: str, lang="en-US"
):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not pathlib.Path(audio_file).exists():
        raise FileNotFoundError(f"{audio_file} doesn't exist")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    audio_source = sr.AudioFile(audio_file)
    with audio_source as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        audio = recognizer.record(source)

    # set up the response object
    response = {"success": True, "error": None, "transcription": None}

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, language=lang)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response
