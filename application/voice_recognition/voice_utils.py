import os
import sys
# from src.exception import CustomException
# from src.logger import logging

from voice_capture import record_audio
PROFILE_DIR = "speaker_profiles"

# voice capture imports 
import sounddevice as sd
import numpy as np
# from src.logger import logging
from scipy.io.wavfile import write


#identification part imports 
import pickle 
import torch 
import librosa
#___import customexceptions 


class VoiceRecognition:
    def __init__(self) -> None:
        pass

    def record_audio(self,duration=5, sample_rate=16000):
        print("Recording audio... Please speak.")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()  # Waiting until recording is finished
        file_path = "test_audio.wav"
        write(file_path, sample_rate, np.int16(recording * 32767))  # Save as a WAV file
        print("Recording complete.")
        return file_path
    
    def enroll_speaker(self,speaker_name, enrollment_audio_file):
        pass


    def identification(self,):
        pass

    
    def list_enrolled(self):
        pass



