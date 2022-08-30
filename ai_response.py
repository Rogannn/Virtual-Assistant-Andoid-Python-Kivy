from recog import sr, speaker

spoken_list = []

recognizer = sr.Recognizer()


def aiResponse(response):
    global recognizer
    # text = main.word_splitter(response)
    spoken_list.append(response)
    # main.update_bot_speech(text)

    try:
        speaker.say(response)
        speaker.runAndWait()
    except RuntimeError:
        recognizer = sr.Recognizer()
        print("RuntimeError, already speaking!")
    except sr.UnknownValueError:
        recognizer = sr.Recognizer()
        print("There was a problem in receiving the words of the speaker, the words might be too unrecognizable.")
