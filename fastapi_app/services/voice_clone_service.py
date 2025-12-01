def clone_voice(path: str):
    print(f"[DEBUG] Voice cloned from: {path}")


def generate_voice_line(text: str):
    return {"audio_file": "shared/voice/generated_audio.wav", "text": text}