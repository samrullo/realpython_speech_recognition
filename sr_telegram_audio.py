import pathlib
import speech_recognition as sr
import time
import sys
from samrullo_speech_recognizer_telegram_bot.sr_utils import (
    recognize_speech_from_audio_file,
)

folder = pathlib.Path(r"C:\Users\amrul\programming\speech_recognition")
audio_file = "telegram_audio_2022-04-24_13-09-24.ogg"

r = sr.Recognizer()

response = recognize_speech_from_audio_file(r, str(folder / audio_file))
print(response["transcription"])
