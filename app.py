from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sys
from application.face_utils import FaceRecognition
from application.voice_utils import VoiceRecognition
from application.customer_manager import Customer
from application.exceptions import CustomException
from speech_module import speak_code

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages

PROFILE_DIR = 'customer_data'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    
    if request.method == 'POST':
        try:
            speak_code("Enrollment process started")
            speak_code("Kindly enter your name")
            # Get the customer name from the form
            customer_name = request.form['name']
            
            if not customer_name:
                flash("Please enter a valid name.")
                return redirect(url_for('enroll'))
            
            
            speak_code("Voice Recording for verification will start after this msg kindly speak any thing for five seconds")
            # Step 1: Record voice
            voice_recognition = VoiceRecognition()
            enrollment_audio_file = voice_recognition.record_audio()
            speak_code("Voice recorded successfully")
            voice_encoding = voice_recognition.extract_voice_embedding(enrollment_audio_file)

            # Step 2: Capture face
            speak_code("Photo capture will start 5 seconds after this msg kindly sit in front of camera and make a smile")
            face_recognition = FaceRecognition()
            face_embedding = face_recognition.capture_face()

            if face_embedding is None:
                speak_code("Face capture failed")
                flash("Face enrollment failed. Try again.")
                return redirect(url_for('enroll'))
            speak_code("Face capture successful")

            # Step 3: Save the customer
            customer = Customer(name=customer_name, face_encoding=face_embedding, voice_encoding=voice_encoding)
            customer.save()

            speak_code(f"{customer_name} has been successfully enrolled!")
            flash(f"{customer_name} has been successfully enrolled!")
            return redirect(url_for('enroll'))

        except Exception as e:
            # Handle any exceptions during the process
            raise CustomException(e, sys)

    return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)
