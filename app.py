from base64 import decodebytes, b64decode
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from tempfile import TemporaryDirectory
from werkzeug.utils import secure_filename
import os
import whisper

load_dotenv()

ALLOWED_EXTENSIONS = set(['flac', 'mp3', 'wav', 'm4a', 'ogg', 'aac', 'ac3', 'wma'])
TEMP_STORAGE = TemporaryDirectory()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['TEMP_STORAGE'] = TEMP_STORAGE

model = whisper.load_model("small")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["POST"])
def speech_to_text():
    content_type = request.headers["Content-Type"].split(';')[0]
    print(content_type)
    if content_type == "multipart/form-data":
        return _stt_form_data_helper()
    elif content_type == "application/json":
        return _stt_json_helper()

def _stt_form_data_helper():
    audio = request.files['audio']
    lang = request.args.get("language")
    if audio.filename == '':
        print('No audio file selected')
        return

    if audio and allowed_file(audio.filename):
        filename = secure_filename(audio.filename)
        audio_path = os.path.join(app.config['TEMP_STORAGE'].name, filename)
        audio.save(audio_path)

        if lang:
            result = model.transcribe(audio_path, fp16=False, verbose=True, language=lang)
            context = jsonify(text=result["text"])
        else:
            result = model.transcribe(audio_path, fp16=False, verbose=True)
            context = jsonify(text=result["text"], language=result['language'])
        print(context.data)

        return context

def _stt_json_helper():
    json_ = request.get_json()
    audio, filename = json_['audio'], json_['filepath'].rsplit('/', 1)[1]
    lang = request.args.get('language')

    if allowed_file(filename):
        filename = secure_filename(filename)
        audio_path = os.path.join(app.config['TEMP_STORAGE'].name, filename)
        
        with open(audio_path, "wb") as f:
            decoded = b64decode(audio.split(',')[1])
            f.write(decoded)

        if lang:
            result = model.transcribe(audio_path, fp16=False, verbose=True, language=lang)
            context = jsonify(text=result["text"])
        else:
            result = model.transcribe(audio_path, fp16=False, verbose=True)
            context = jsonify(text=result["text"], language=result['language'])
        print(context.data)

        return context

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
    TEMP_STORAGE.cleanup()
    app.config['TEMP_STORAGE'].cleanup()
