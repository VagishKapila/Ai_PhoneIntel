from fastapi import APIRouter, File, UploadFile, Form
from fastapi_app.services.voice_clone_service import clone_voice, generate_voice_line

router = APIRouter()

@router.post("/clone")
async def voice_clone(file: UploadFile = File(...)):
    file_path = f"shared/voice/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    clone_voice(file_path)
    return {"message": "Voice cloned successfully!"}

@router.post("/generate")
async def voice_generate(line: str = Form(...)):
    output = generate_voice_line(line)
    return {"audio": output}