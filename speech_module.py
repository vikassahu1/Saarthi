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
            
def listen_for_command2():
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
        
# For enrollment part only def listen_for_letter():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a letter...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            # Use phrase hints to improve accuracy for letters
            letter = recognizer.recognize_google(audio, show_all=False)
            print(f"You said: {letter}")
            
            if letter and len(letter) == 1 and letter.isalpha():
                return letter.upper()
            else:
                print("Please say a single letter.")
                return None
        except sr.UnknownValueError:
            print("Sorry, I could not understand the input.")
        except sr.RequestError:
            print("There is an issue with the recognition service.")
        return None


def capture_full_name():
    speak_code("Please say your full name.")
    name = listen_for_command2()
    if name:
        speak_code(f"You said: {name}. Say continue to proceed ")
        if listen_for_command2().lower() == "continue":
            return name
    speak_code("Let's try again.")
    return capture_full_name()


def confirm_name(name):
    while True:
        speak_code(f"Your name is spelled as {name}. Please say continue to confirm or again to re-enter.")
        confirmation = listen_for_command2()
        if confirmation and confirmation.lower() == "continue":
            return True
        elif confirmation and confirmation.lower() == "again":
            return False
        else:
            speak_code("Please say coninue or again.")