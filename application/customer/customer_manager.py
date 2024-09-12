import os
import pickle 

class Customer:
    def __init__(self, name, face_encoding=None, voice_encoding=None):
        self.name = name
        self.face_encoding = face_encoding
        self.voice_encoding = voice_encoding

    def save(self):
        # Save customer data (name, face, and voice encodings) in a single .pkl file
        data = {
            'name': self.name,
            'face_encoding': self.face_encoding,
            'voice_encoding': self.voice_encoding
        }
        with open(f'customer_data/{self.name}.pkl', 'wb') as f:
            pickle.dump(data, f)


    # classmethod is used to directly return class inststance and takes class(cls) as input 
    # through this we can dirctly call methods of the functions without using its instance.
    # Can be used for factory methods :  factory methods that return an instance of the class after doing some operations.
    @classmethod
    def load(cls, name):
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
    