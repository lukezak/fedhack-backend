# -*- coding: utf-8 -*-

"""
    BioMedic - API
    ~~~~~~~~
"""

import logging, os
from eve import Eve
from flask import url_for, send_from_directory, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import face_recognition
import uuid


# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    # use '0.0.0.0' to ensure your REST API is reachable from all your
    # network (and not only your computer).
    host = '0.0.0.0'
else:
    port = 5000
    host = '127.0.0.1'

app = Eve()
CORS(app)

"""x
    Configuration
"""
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
KNOWN_FOLDER = '{}/known/'.format(PROJECT_HOME)
UNKNOWN_FOLDER = '{}/unknown/'.format(PROJECT_HOME)
app.config['KNOWN_FOLDER'] = KNOWN_FOLDER
app.config['UNKNOWN_FOLDER'] = UNKNOWN_FOLDER

"""
    Helpers
"""
def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

def match_face(image):
    img_data = image
    new_uuid = uuid.uuid4()
    temp_name = str(new_uuid)
    img_name = secure_filename(temp_name + '.jpg')
    create_new_folder(app.config['UNKNOWN_FOLDER'])
    saved_path = os.path.join(app.config['UNKNOWN_FOLDER'], img_name)
    with open(saved_path, "wb") as fh:
            fh.write(img_data.decode('base64'))
    app.logger.info("saving {}".format(saved_path))
    directory = app.config['KNOWN_FOLDER']
    unknown_face = face_recognition.load_image_file(saved_path)
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"): 
            fullpath = os.path.join(directory, filename)
            known_face = face_recognition.load_image_file(fullpath)
            try:
                known_face_encoding = face_recognition.face_encodings(known_face)[0]
                unknown_face_encoding = face_recognition.face_encodings(unknown_face)[0]
            except IndexError:
                return("Unable to locate any faces in the image. Check the image file.")
            known_faces = [
                known_face_encoding
            ]
            result = face_recognition.compare_faces(known_faces, unknown_face_encoding)
            if result[0] == True:
                return os.path.splitext(filename)[0]
            else:
                continue
        else:
            continue
    return "False"

def save_face(image):
    app.logger.info("saving image")
    img_data = image
    user_id = str(uuid.uuid4())    
    img_name = secure_filename(user_id + '.jpg')
    create_new_folder(app.config['KNOWN_FOLDER'])
    saved_path = os.path.join(app.config['KNOWN_FOLDER'], img_name)
    with open(saved_path, "wb") as fh:
            fh.write(img_data.decode('base64'))
    app.logger.info("saving {}".format(saved_path))
    return user_id

"""
    Custom End-points
"""
@app.route('/', methods = ['GET'])
def api_root():
    return "BioMedic (Fedhacker!) Medic"

@app.route('/auth', methods = ['POST'])
def auth():
    app.logger.info("AuthN AuthZ user by image")
    img_data = request.form['image']
    img_data = img_data.replace('data:image/jpeg;base64,', '')
    return match_face(img_data)

@app.route('/register', methods = ['POST'])
def api_register():
    app.logger.info("Registering user")
    img_data = request.form['image']
    img_data = img_data.replace('data:image/jpeg;base64,', '')
    return save_face(img_data)

if __name__ == '__main__':
    app.run(host=host, port=port)
