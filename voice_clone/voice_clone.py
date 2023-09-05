from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import requests
import tempfile
import os
from pydub import AudioSegment

app = FastAPI()

def validate_audio_files(audio_files):
    for audio_file in audio_files:
        duration = AudioSegment.from_file(audio_file.file).duration_seconds
        if duration < 50:
            raise HTTPException(status_code=400, detail=f"Audio file {audio_file.filename} should be at least 50 seconds long.")

@app.post("/clone_voice/")
async def clone_voice(
    name: str = Form(...),
    labels: str = Form(...),
    description: str = Form(...),
    audio_files: list[UploadFile] = File(...)
):
    url = "https://api.elevenlabs.io/v1/voices/add"

    headers = {
        "Accept": "application/json",
        "xi-api-key": "<xi-api-key>"
    }

    data = {
        "name": name,
        "labels": labels,
        "description": description
    }

    try:
        validate_audio_files(audio_files)

        temp_files = []
        for audio_file in audio_files:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(audio_file.file.read())
            temp_file.close()
            temp_files.append(temp_file.name)

        files = [
            ('files', (os.path.basename(temp_file), open(temp_file, 'rb'), audio_file.content_type)) for temp_file in temp_files
        ]

        response = requests.post(url, headers=headers, data=data, files=files)
        response.raise_for_status()

        for temp_file in temp_files:
            os.remove(temp_file)

        return {"message": "Voice clone successful", "response": response.text}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Voice clone failed")
