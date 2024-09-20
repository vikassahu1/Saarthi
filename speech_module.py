import pyttsx3
import speech_recognition as sr

def speak_code(code):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty('voices')

    # Set the female voice (usually voice[1] is female)
    engine.setProperty('voice', voices[1].id)

    # Set the speech rate (optional)
    engine.setProperty('rate', 150)

    # Speak the code
    engine.say(code)
    
    # Run the engine
    engine.runAndWait()


def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            speak_code("Sorry, I could not understand your command. Please try again.")
            return ""
        except sr.RequestError:
            speak_code("Sorry, there was an error with the speech recognition service.")
            return ""