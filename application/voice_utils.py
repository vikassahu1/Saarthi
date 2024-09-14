import os
import sys
import pickle
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import librosa
import torch
from speechbrain.pretrained import SpeakerRecognition
from exceptions import CustomException

verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models")

PROFILE_DIR = 'customer_data'

class VoiceRecognition:
    def __init__(self):
        pass

    def record_audio(self, duration=5, sample_rate=16000):
        """
        Records audio for a specific duration and returns the path to the saved audio file.
        """
        try:
            if not os.path.exists(PROFILE_DIR):
                os.makedirs(PROFILE_DIR)

            print("Recording audio... Please speak.")
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
            sd.wait()  
            file_path = f"temp_voice.wav"
            write(file_path, sample_rate, np.int16(recording * 32767))  
            print("Recording complete.")
            return file_path
        except Exception as e:
            raise CustomException(e, sys)


    def extract_voice_embedding(self, audio_file):
        try:
            # Load the audio file
            waveform, sr = librosa.load(audio_file, sr=None)
            # waveform_tensor = torch.tensor(waveform).unsqueeze(0)  # Converting to torch tensor (1, samples)
            waveform = np.expand_dims(waveform, axis=0)

            # Ensure proper tensor shape before encoding
            voice_embedding = verification.encode_batch(torch.tensor(waveform)) # Squeeze after encoding
            
            return voice_embedding
        except Exception as e:
            raise CustomException(e, sys)


    def load_speaker_profile(self, profile_path):
        """
        Loads a speaker profile from the given pickle file.
        """
        try:
            with open(profile_path, 'rb') as f:
                profile = pickle.load(f)
            return profile
        except Exception as e:
            raise CustomException(e,sys)


    def identify_speaker(self, test_audio_file_path):
        """
        Identifies the speaker from the provided test audio file by comparing the voice embeddings using cosine similarity.
        """
        try:
            # Load and process the test audio
            waveform, sample_rate = librosa.load(test_audio_file_path, sr=None)
            waveform_tensor = torch.tensor(waveform) # Ensure (1, samples) shape

            # Encode the test audio file to get the embedding
            test_embedding = verification.encode_batch(waveform_tensor.unsqueeze(0)).squeeze().cpu().detach().numpy()

            # Initialize best match variables
            best_score = -float('inf')
            identified_speaker = None

            # Iterate over enrolled speakers' profiles and compare embeddings
            for profile_file in os.listdir(PROFILE_DIR):
                profile_path = os.path.join(PROFILE_DIR, profile_file)
                profile = self.load_speaker_profile(profile_path)

                # Calculate cosine similarity between embeddings
                score = np.dot(test_embedding, profile['voice_encoding']) / (np.linalg.norm(test_embedding) * np.linalg.norm(profile['voice_encoding']))

                # Update the best match based on the score
                if score > best_score:
                    best_score = score
                    identified_speaker = profile['name']

            # Return the identified speaker if the score exceeds a threshold
            if best_score > 0.5:
                return identified_speaker
            else:
                return None
        except Exception as e:
            raise CustomException(e, sys)
