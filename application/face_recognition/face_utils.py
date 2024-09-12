import cv2
import torch
import pickle
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(keep_all=False, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)


class FaceRecognition:
    def __init__(self) -> None:
        pass

    def capture_face(self):
        cap = cv2.VideoCapture(0)
        face_embedding = None

        if not cap.isOpened():
            print("Error: Could not open camera.")
            return None

        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image.")
                break

            # Show the frame
            cv2.imshow('Scanning Face', frame)

            # Convert frame to PIL image for processing
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Detect face and get embedding
            face = mtcnn(img)
            if face is not None:
                face_embedding = resnet(face.unsqueeze(0)).detach().cpu()
                print("Face detected!")
                break  # Exit 

            # Opening the camera after 5 seconds
            if time.time() - start_time > 5:
                print("Timeout: No face detected within 5 seconds.")
                break

            # To ensure the frame window is visible
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return face_embedding



    # Function used to load all the face embeddings in the program   
    # To make : load and save functions 
    def load_known_faces(self):
        return [],[]



    # register function will be in main code 
    def verify_face(self):
        known_face_encodings, known_face_names = self.load_known_faces()

        print("Verifying user. Camera will be open for 5 seconds.")
        face_embedding = self.capture_face()

        if face_embedding is None:
            print("Face not detected. Please try again.")
            return

        # Compare captured face embedding to known faces
        distances = [torch.dist(face_embedding, known_face).item() for known_face in known_face_encodings]
        
        if distances:
            min_distance = min(distances)
            best_match_index = distances.index(min_distance)

            # Threshold for verification
            if min_distance < 0.7:
                print(f"Verified! Welcome back, {known_face_names[best_match_index]}")
            else:
                print("Face not recognized. Please try again.")
        else:
            print("No faces registered yet.")



    # Register face function is yet to be made 
    