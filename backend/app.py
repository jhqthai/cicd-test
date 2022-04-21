from time import sleep
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask_cors import CORS, cross_origin
import stt
import os
from werkzeug.utils import secure_filename

# APP id integration sample : https://github.com/mnsn/appid-python-flask-example/blob/master/Validation%20with%20token%20introspection%20endpoint/welcome.py
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp3'}
FILENAME = ""

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = "gfd"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1000 * 1000


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/transcribe/download-csv/<string:name>', methods=['GET'])
def download_transcript(name):
    filename = name
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# *** parse the csv file from stt to app.py as a post request
@app.route('/transcribe/upload-audio', methods=['POST'])
def upload_file():
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # audio_file = file
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        FILENAME = os.path.splitext(file.filename)[0] +".csv"
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            temp_csv_string_stream = stt.main(file)
            file.close()
            sleep(2)
            return temp_csv_string_stream.getvalue(), 200, {'Content-Disposition': f'attachment; filename={FILENAME}; filename*={FILENAME}', 'Content-Type': 'application/octet-stream; charset=utf-8'}