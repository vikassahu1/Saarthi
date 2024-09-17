import os
import sys
from .face_utils import FaceRecognition
from .voice_utils import VoiceRecognition
from .customer_manager import Customer
from .exceptions import CustomException

PROFILE_DIR = 'customer_data'


def list_enrolled_customers():
    """
    List all enrolled customers by checking the customer_data directory.
    """
    try:
        customers = []
        for file in os.listdir(PROFILE_DIR):
            if file.endswith(".pkl"):
                customers.append(file.replace(".pkl", ""))
        return customers
    except Exception as e:
        raise CustomException(e,sys)



def main():
    try:
        if not os.path.exists(PROFILE_DIR):
            os.makedirs(PROFILE_DIR)

        print("Welcome to the Saarthi Payment System")

        while True:
            print("\nOptions:")
            print("1. Enroll a new customer")
            print("2. Verify a customer (voice + face)")
            print("3. List enrolled customers")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                customer_name = input("Enter the customer's name: ")

                # Voice recognition
                print("Recording the customer's voice for enrollment...")
                voice_recognition = VoiceRecognition()
                enrollment_audio_file = voice_recognition.record_audio()
                voice_encoding = voice_recognition.extract_voice_embedding(enrollment_audio_file)

                # Face recognition
                print("Capturing the customer's face for enrollment...")
                face_recognition = FaceRecognition()
                face_embedding = face_recognition.capture_face()

                if face_embedding is None:
                    print("Face enrollment failed. Try again.")
                else:
                    customer = Customer(name=customer_name, face_encoding=face_embedding,  voice_encoding=voice_encoding)
                    customer.save()

                    print(f"{customer_name} has been successfully enrolled!")

            elif choice == '2':
                print("Verifying customer using voice and face...")
                verify_customer()

            elif choice == '3':
                customers = list_enrolled_customers()
                if customers:
                    print(f"Enrolled Customers: {', '.join(customers)}")
                else:
                    print("No customers enrolled yet.")

            elif choice == '4':
                print("Exiting the system.")
                break

            else:
                print("Invalid option, please try again.")

    except Exception as e:
        raise CustomException(e, sys)

def verify_customer():
    # Verification using voice and face
    voice_recognition = VoiceRecognition()
    face_recognition = FaceRecognition()

    print("Recording the customer's voice for verification...")
    test_audio_file = voice_recognition.record_audio()
    # test_voice_encoding = voice_recognition.extract_voice_embedding(test_audio_file)


    print("Capturing the customer's face for verification...")
    face_embedding = face_recognition.capture_face()

    if face_embedding is None:
        print("Face verification failed.")
        return

    # Compare voice and face data for verification  
    speaker1 = voice_recognition.identify_speaker(test_audio_file)
    speaker2 = face_recognition.verify_face(face_embedding)
    print(speaker1)
    print(speaker2)

    if(speaker1==speaker2):
        print("Voice Recognised! Name: ",speaker1)
    elif(speaker1==None):
        print("Voice not Recognised!")
    elif(speaker2==None):
        print("Face not matched!")
    elif(speaker2==-1):
        print("Face not in data")
    else:
        print("Try Again ! Speaker not recognised !")



if __name__ == '__main__':
    main()
