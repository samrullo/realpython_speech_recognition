import speech_recognition as sr

r=sr.Recognizer()

harvard_audio_file=sr.AudioFile("audio_files_harvard.wav")
with harvard_audio_file as source:
    harvard_audio_data=r.record(source)

r.recognize_google(harvard_audio_data)