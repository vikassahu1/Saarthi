from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sys
import time
from flask import jsonify 
from application.face_utils import FaceRecognition
from application.voice_utils import VoiceRecognition
from application.customer_manager import Customer
from application.exceptions import CustomException
from speech_module import speak_code,listen_for_command

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages
PROFILE_DIR = 'customer_data'


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/assist', methods=['POST'])
def assist():
    time.sleep(1)
    speak_code("We are on menu page . You can say 'register me', 'verify me', or 'about us'.")

    # Listen for the user's command
    command = listen_for_command()
    print(f"Command received: {command}")

    # Determine the URL based on the command
    if 'register' in command.lower():
        speak_code("Redirecting to register page")
        return jsonify({'redirect_url': url_for('enroll')})
    elif 'verify' in command.lower():
        speak_code("Redirecting to verify page")
        return jsonify({'redirect_url': url_for('verify')})
    elif 'about' in command.lower():
        speak_code("Redirecting to about page")
        return jsonify({'redirect_url': url_for('about')})
    else:
        speak_code("Sorry, I didn't understand. Please say 'register', 'verify', or 'about us'.")
        return jsonify({'redirect_url': url_for('index')})




# Enrollment part 
@app.route('/enroll', methods=['GET', 'POST'])
def enroll():  
    if request.method == 'GET':
        return render_template('enroll.html')
    if request.method == 'POST':
        try:
            # speak_code("Enrollment process started")
            # speak_code("Kindly enter your name")
            # Get the customer name from the form




            customer_name = request.form['name']
            
            if not customer_name:
                flash("Please enter a valid name.")
                return redirect(url_for('enroll'))
            
            
            speak_code("Voice Recording for verification will start after this msg. Kindly speak any thing for five seconds")
            # Step 1: Record voice
            voice_recognition = VoiceRecognition()
            enrollment_audio_file = voice_recognition.record_audio()
            speak_code("Voice recorded successfully")
            voice_encoding = voice_recognition.extract_voice_embedding(enrollment_audio_file)

            # Step 2: Capture face
            time.sleep(0.5)
            speak_code("Photo capture will start 5 seconds after this msg. Kindly sit in front of camera and make a smile")
            face_recognition = FaceRecognition()
            face_embedding = face_recognition.capture_face()

            if face_embedding is None:
                speak_code("Face capture failed")
                flash("Face enrollment failed. Try again.")
                return redirect(url_for('index'))
            time.sleep(0.5)
            speak_code("Face captured successfully")

            # Step 3: Save the customer
            customer = Customer(name=customer_name, face_encoding=face_embedding, voice_encoding=voice_encoding)
            customer.save()

            speak_code(f"{customer_name} has been successfully enrolled!")
            flash(f"{customer_name} has been successfully enrolled!")
            return redirect(url_for('index'))

        except Exception as e:
            # Handle any exceptions during the process
            raise CustomException(e, sys)
    return render_template('enroll.html')





# Verification part 
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        try:
            # Start the verification process
            speak_code("We are on verification page")

            # Step 1: Record voice for verification
            speak_code("Voice recording for verification will start after this message. Kindly speak anything for five seconds")
            voice_recognition = VoiceRecognition()
            test_audio_file = voice_recognition.record_audio()
            speak_code("Voice recorded successfully")
            
            # Step 2: Capture face for verification
            time.sleep(0.5)
            speak_code("Photo capture will start 5 seconds after this message. Kindly sit in front of the camera and make a smile")
            face_recognition = FaceRecognition()
            face_embedding = face_recognition.capture_face()

            if face_embedding is None:
                speak_code("Face capture failed")
                flash("Face verification failed. Try again.")
                return jsonify({'redirect_url': url_for('verify')})

            time.sleep(0.5)
            speak_code("Face captured successfully")

            # Step 3: Identify speaker using voice and face data
            speaker_name_from_voice = voice_recognition.identify_speaker(test_audio_file)
            speaker_name_from_face = face_recognition.verify_face(face_embedding)

            # Handle verification results
            if speaker_name_from_voice == speaker_name_from_face and speaker_name_from_voice is not None:
                speak_code(f"Verification successful! Welcome {speaker_name_from_voice}")
                flash(f"Verification successful! Welcome {speaker_name_from_voice}")
                
                # Return the redirect URL as JSON for the frontend to handle
                return jsonify({'redirect_url': url_for('welcome', name=speaker_name_from_voice)})
            else:
                if speaker_name_from_voice is None:
                    speak_code("Voice not recognized")
                    flash("Voice not recognized")
                if speaker_name_from_face is None:
                    speak_code("Face not recognized")
                    flash("Face not recognized")
                if speaker_name_from_face == -1:
                    speak_code("Face not found in the database")
                    flash("Face not found in the database")
                else:
                    speak_code("Verification failed, please try again.")
                    flash("Verification failed, please try again.")
                return jsonify({'redirect_url': url_for('verify')})

        except Exception as e:
            # Handle any exceptions during the verification process
            raise CustomException(e, sys)

    return render_template('verify.html')




# About section 
@app.route('/about')
def about():
    about_text = "Welcome to Saarthi Payment System. We are dedicated to providing secure and convenient payment solutions through voice and face recognition. Our system ensures seamless customer verification, combining cutting-edge technology with a user-friendly experience."
    
    # Render the 'about.html' template with the about text
    return render_template('about.html', about_text=about_text)

@app.route('/speak_about_text', methods=['POST'])
def speak_about_text():
    try:
        data = request.get_json()
        text_to_speak = data.get('text')
        
        speak_code(text_to_speak)
        return redirect(url_for('index'))
    except Exception as e:
        raise CustomException(e, sys)




@app.route('/welcome',methods=['POST','GET'])
def welcome():
    name = request.args.get('name')
    return render_template('welcome.html',name=name)



if __name__ == '__main__':
    app.run(debug=True)