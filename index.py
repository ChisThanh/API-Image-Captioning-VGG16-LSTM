from flask import Flask, Blueprint, jsonify, request, send_file
from flask_cors import CORS 
from googletrans import Translator

from generate_description import load_max_length, load_tokenizer, load_caption_model, load_and_prepare_photograph, generate_description
from speaking_doc import speaking
import base64
import os
from keras.models import load_model

app = Flask(__name__)
CORS(app)

model_input = load_model('vgg16_model.keras')
max_length = load_max_length()
model = load_caption_model()
tokenizer = load_tokenizer()

TMP_FOLDER = 'tmp'

def translate_text(text, dest='vi'):
    translator = Translator()
    result = translator.translate(text, dest)
    return result.text

def save_uploaded_file(file):
    file_path = os.path.join(TMP_FOLDER, file.filename)
    file.save(file_path)
    return file_path

def cleanup_tmp_file(file_path):
    os.remove(file_path)

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1/')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/', methods=['GET'])
def index_home():
    return jsonify({'error': 'GET method is not supported'}), 400

@api_v1.route('/auto-create-caption', methods=['GET'])
def index():
    return jsonify({'error': 'GET method is not supported'}), 400


@api_v1.route('/auto-create-caption', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    file_path = save_uploaded_file(file)
    try:
        photo = load_and_prepare_photograph(file_path, model_input)
        description = generate_description(model, tokenizer, photo, max_length)

        path_en = speaking(description, 'en')
        path_vi = speaking(translate_text(description), 'vi')

        with open(path_en, 'rb') as file_audio:
            audio_en = base64.b64encode(file_audio.read()).decode()

        with open(path_vi, 'rb') as file_audio:
            audio_vi = base64.b64encode(file_audio.read()).decode()

        return jsonify({
                'success': True,
                'en': {
                    'text': description,
                    'file': audio_en
                },
                'vi': {
                    'text': translate_text(description),
                    'file': audio_vi
                },
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cleanup_tmp_file(file_path)
        cleanup_tmp_file(path_en)
        cleanup_tmp_file(path_vi)


app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
