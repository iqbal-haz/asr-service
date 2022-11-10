from dotenv import load_dotenv
from flask import Flask, request, jsonify
from tempfile import TemporaryDirectory
from werkzeug.utils import secure_filename
import os
import whisper

load_dotenv()

ALLOWED_EXTENSIONS = set(['flac', 'mp3', 'wav', 'm4a', 'ogg', 'aac', 'ac3', 'wma'])
UPLOAD_FOLDER = TemporaryDirectory()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = whisper.load_model("small")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["POST"])
def speech_to_text():
    audio = request.files['audio']
    if audio.filename == '':
        print('No audio file selected')
        return

    if audio and allowed_file(audio.filename):
        filename = secure_filename(audio.filename)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'].name, filename)
        audio.save(audio_path)

        result = model.transcribe(audio_path, fp16=False)
        context = jsonify(text=result["text"])
        print(context.data)

        return context

if __name__ == "__main__":
    app.run()
    UPLOAD_FOLDER.cleanup()
    app.config['UPLOAD_FOLDER'].cleanup()
