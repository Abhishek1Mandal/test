from fastapi import FastAPI, UploadFile, File, Form
from whisper.utils import get_writer
from deep_translator import GoogleTranslator
import whisper
import os
from base64 import b64encode
from IPython.display import Audio, HTML

from Transcript.Mp4_sub import translate_vtt

app = FastAPI()


# Other code and routes...

@app.post("/generate_and_translate_subtitles/")
async def generate_and_translate_subtitles_route(
        audio_file: UploadFile = File(...),
        TARGET_LANG_CODE: str = 'de',
        SUBTITLE_TYPE: str = 'vtt',
):
    try:
        # Load your ASR model (adjust this as needed)
        MODEL_SIZE = 'medium'
        model = whisper.load_model(MODEL_SIZE)

        # Transcribe the audio
        transcription = model.transcribe(audio_file)

        # Translate the transcription to English
        translator = GoogleTranslator(source='auto', target='en')
        translated_transcription = translator.translate(transcription)

        # Make subtitles
        options = {
            "max_line_width": 12,
            "max_line_count": 1,
            "highlight_words": 12
        }
        output_writer = get_writer(SUBTITLE_TYPE, '.')
        output_writer(translated_transcription, 'subtitles_en', options)
        subtitles_path = f'subtitles_en.{SUBTITLE_TYPE}'

        # Translate subtitles if needed
        if TARGET_LANG_CODE != 'en' and subtitles_path[:-4] != '.srt':
            try:
                translate_vtt(TARGET_LANG_CODE, subtitles_path)
            except:
                return {"error": f'Invalid TARGET_LANG_CODE: {TARGET_LANG_CODE}. Generating subtitles in English'}
        else:
            print('Generating subtitles in English')

        # Provide the path to the generated subtitles
        return {"subtitles_path": subtitles_path}
    except Exception as e:
        return {"error": str(e)}

# Rest of the code...
