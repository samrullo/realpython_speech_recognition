import speech_recognition as sr

r = sr.Recognizer()

jackhammer = sr.AudioFile("audio_files_jackhammer.wav")

with jackhammer as source:
    audio = r.record(source)

r.recognize_google(audio)
