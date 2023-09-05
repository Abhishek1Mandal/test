from flask import Flask, request, jsonify, render_template, send_from_directory
import logging
from werkzeug.utils import secure_filename
from tempfile import NamedTemporaryFile
import os
from text_images.image_genration import process_image
from text_music.music import generate_music
from text_chart import chart
from Transcript.Youtube_video_sub import process_video
from Transcript.Youtube_sub import process_youtube_subtitles
from Transcript.Youtube_Mp4 import process_youtube_video
from Transcript.Mp4_Mp3 import process_video_to_audio
from Transcript.Mp4_video_sub import process_video_with_subtitles
from Transcript.Mp4_sub import process_video_and_return_subtitles
from Transcript.Mp3_sub import generate_and_translate_subtitles_route
from text_voice import text_voice
from voice_clone import voice_clone

app = Flask(__name__)

# Create a logger instance
logger = logging.getLogger(__name__)

# Set the logging level (You can adjust this as needed)
logger.setLevel(logging.DEBUG)

# Create a file handler to log to a file (optional)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler to log to the console (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter to specify the log message format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Define allowed origins for CORS (Replace with your frontend URL)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

# Enable CORS for the Flask app
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return 'Welcome to the Flask app!'


@app.route('/api/image_generation/process_image', methods=['POST'])
def call_process_image():
    prompt = request.json.get('prompt')
    image_result = process_image(prompt)
    return jsonify(image_result)


@app.route('/api/music_gen/generate_music', methods=['POST'])
def call_generate_music():
    prompts = request.json.get('prompts')
    duration = request.json.get('duration')
    music_response = generate_music(prompts, duration)
    return jsonify(music_response)


@app.route('/api/pie_chart/generate_pie_chart', methods=['POST'])
def call_generate_pie_chart():
    instruction = request.json.get('instruction')
    generated_text = chart.generate_pie_chart(instruction)
    return jsonify({"result": generated_text})


@app.route('/insert_user/', methods=['POST'])
def insert_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    phone_number = request.form['phone_number']
    email = request.form['email']
    
    try:
        logger.info("Received data: %s, %s, %s, %s, %s", first_name, last_name, username, phone_number, email)

        # Call the insert_user_data function from login.py to insert data into MongoDB
        result = insert_user_data(first_name, last_name, username, phone_number, email)

        return jsonify({"message": result})
    except Exception as e:
        logger.error("Error processing insert_user request: %s", str(e))
        return jsonify({"error": "An error occurred while processing the request."})


@app.route('/process_youtube_video/', methods=['POST'])
def process_youtube_video_route():
    video_file = request.files['video_file']
    target_lang_code = request.form['target_lang_code']
    subtitle_type = request.form['subtitle_type']

    try:
        # Save the uploaded video
        temp_video = NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video.write(video_file.read())
        video_path = temp_video.name

        # Process video using functions from Youtube_video_sub.py
        response = process_video(video_path, target_lang_code, subtitle_type)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/process_youtube_sub/', methods=['POST'])
def process_youtube_sub():
    youtube_url = request.form['youtube_url']
    target_lang_code = request.form['target_lang_code']
    subtitle_type = request.form['subtitle_type']

    try:
        subtitles_file = process_youtube_subtitles(youtube_url, target_lang_code, subtitle_type)
        # Return a response indicating success
        return jsonify({"message": "Subtitles processed and translated successfully", "subtitles_file": subtitles_file})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/process_youtube_video/', methods=['POST'])
def process_youtube_video():
    youtube_url = request.form['youtube_url']
    TARGET_LANG_CODE = request.form['TARGET_LANG_CODE']
    SUBTITLE_TYPE = request.form['SUBTITLE_TYPE']
    MODEL_SIZE = 'medium'  # Set the desired model size here

    try:
        result = process_youtube_video(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE)
        # Return a response indicating success
        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/convert_video_to_audio/', methods=['POST'])
def convert_video_to_audio_route():
    video_path = request.form['video_path']

    try:
        audio_path = process_video_to_audio(video_path)
        # Return a response indicating success
        return jsonify({"message": "Video converted to audio successfully", "audio_path": audio_path})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/process_video_with_subtitles/', methods=['POST'])
def process_video_with_subtitles_route():
    youtube_url = request.form['youtube_url']
    MODEL_SIZE = 'medium'  # Set the desired model size here
    TARGET_LANG_CODE = 'de'
    SUBTITLE_TYPE = 'vtt'

    try:
        output_video_path = process_video_with_subtitles(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE)
        # Display the video with subtitles (Note: This part may need modification)
        return jsonify({"message": "Video processed and subtitled successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/process_video_and_get_subtitles/', methods=['POST'])
def process_video_and_get_subtitles_route():
    youtube_url = request.form['youtube_url']
    MODEL_SIZE = 'medium'  # Set the desired model size here
    TARGET_LANG_CODE = 'de'
    SUBTITLE_TYPE = 'vtt'

    try:
        subtitles = process_video_and_return_subtitles(youtube_url, MODEL_SIZE, TARGET_LANG_CODE, SUBTITLE_TYPE)
        # Return the generated subtitles
        return jsonify({"subtitles": subtitles})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/process_audio_and_get_subtitles/', methods=['POST'])
def process_audio_and_get_subtitles_route():
    audio_file = request.files['audio_file']
    TARGET_LANG_CODE = 'de'
    SUBTITLE_TYPE = 'vtt'

    try:
        response = generate_and_translate_subtitles_route(audio_file, TARGET_LANG_CODE, SUBTITLE_TYPE)
        return response
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/convert/', methods=['POST'])
def convert_text_to_speech():
    voice_id = request.form['voice_id']
    text = request.form['text']

    result = text_voice.convert_text_to_speech(voice_id, text)
    return jsonify(result)


@app.route('/clone_voice/', methods=['POST'])
def clone_voice():
    name = request.form['name']
    labels = request.form['labels']
    description = request.form['description']
    audio_files = request.files.getlist('audio_files')

    return voice_clone.clone_voice(name, labels, description, audio_files)


# Serve static files (CSS, JS, images, etc.) from the "static" directory
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(port=8000)
