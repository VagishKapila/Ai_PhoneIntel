from TTS.api import TTS
import os
import uuid

VOICE_MODEL = "tts_models/multilingual/multi-dataset/your_tts"
tts = TTS(VOICE_MODEL)

VOICE_REF = "shared/voice/reference.wav"

def clone_voice(path):
    os.system(f"cp {path} {VOICE_REF}")

def generate_voice_line(text):
    output = f"shared/jobs/audio/{uuid.uuid4()}.wav"
    tts.tts_to_file(text=text, speaker_wav=VOICE_REF, file_path=output)
    return output