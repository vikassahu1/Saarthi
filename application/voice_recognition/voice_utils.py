import os
import sys
# from src.exception import CustomException
# from src.logger import logging
from enrolment import enroll_speaker, list_enrolled_speakers
from identification import identify_speaker
from voice_capture import record_audio
PROFILE_DIR = "speaker_profiles"


class VoiceRecognition:
    def __init__(self) -> None:
        pass

    