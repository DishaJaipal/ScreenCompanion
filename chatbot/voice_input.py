<<<<<<< HEAD
import speech_recognition as sr

def listen_to_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."



=======
import speech_recognition as sr

def listen_to_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
>>>>>>> 86744fa57c56d37e6c25bbf0d94906edc8deb6e5
