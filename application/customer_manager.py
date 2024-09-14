import os
import pickle

PROFILE_DIR = 'customer_data'

class Customer:
    def __init__(self, name, face_encoding=None, voice_encoding=None):
        self.name = name
        self.face_encoding = face_encoding
        self.voice_encoding = voice_encoding

    def save(self):
        try:
            profile_path = os.path.join(PROFILE_DIR, f"{self.name}.pkl")
            with open(profile_path, 'wb') as f:
                pickle.dump({'name': self.name, 'face_encoding': self.face_encoding, 'voice_encoding': self.voice_encoding.squeeze().cpu().detach().numpy()}, f)
            print(f"Customer {self.name} saved successfully!")
        except Exception as e:
            print(f"Error saving customer {self.name}: {e}")


    @classmethod
    def load(cls, name):
        # Load customer data from the .pkl file
        try:
            with open(f'customer_data/{name}.pkl', 'rb') as f:
                data = pickle.load(f)
                return cls(name, data['face_encoding'], data['voice_encoding'])
        except FileNotFoundError:
            return None


    def update_face_encoding(self, face_encoding):
        self.face_encoding = face_encoding
        self.save()


    def update_voice_encoding(self, voice_encoding):
        self.voice_encoding = voice_encoding
        self.save()
