import speech_recognition as sr
import time

r=sr.Recognizer()

jackhammer=sr.AudioFile("audio_files_jackhammer.wav")

with jackhammer as source:
    r.adjust_for_ambient_noise(source,duration=0.5)
    audio=r.record(source)

time.sleep(2)
r.recognize_google(audio,show_all=True)