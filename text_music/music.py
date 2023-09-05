from audiocraft.models import musicgen
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
from typing import List
import torch

# Load the music generation model
model = musicgen.MusicGen.get_pretrained('large', device='cuda')


def generate_music(prompts: List[str], duration: int):
    if not prompts or not duration:
        return {"error": "Invalid request. Please provide prompts and duration."}

    # Set the duration for music generation
    model.set_generation_params(duration=duration)

    # Generate the audio using the model
    res = model.generate(prompts, progress=True)

    # Save the generated audio to a temporary file
    with NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        audio_path = temp_audio_file.name
        res.save(audio_path, 32000)

    return FileResponse(audio_path, filename='generated_audio.wav')

# You can add more functions and code related to image generation here
