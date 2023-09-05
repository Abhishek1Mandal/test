from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

CHUNK_SIZE = 1024


@app.post("/convert_text_to_speech/")
async def convert_text_to_speech(voice_id: str, text: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "<xi-api-key>"
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        output_filename = f"{voice_id}_output.mp3"
        with open(output_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

        return {"message": "Text-to-speech conversion successful", "output_filename": output_filename}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Text-to-speech conversion failed")
