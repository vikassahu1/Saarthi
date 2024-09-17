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


def listen_to_speech():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Please speak...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        # Capture the audio from the microphone
        audio = recognizer.listen(source)

    try:
        # Use Google Web Speech API to recognize the speech
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Sorry, the speech recognition service is unavailable.")

# Example usage
if __name__ == "__main__":
    speak_code("Speak the bitch")
    listen_to_speech()
