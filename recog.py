import speech_recognition as sr
import pyttsx3 as tts

recognizer = sr.Recognizer()

# TTS setup
speaker = tts.init()
speaker.setProperty('rate', 150)
voices = speaker.getProperty('voices')
# voices[0] = male, voices[1] = female
speaker.setProperty('voice', voices[0].id)
