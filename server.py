from flask import Flask, url_for, send_from_directory, request
from flask_cors import CORS
import logging, os
from werkzeug.utils import secure_filename
import face_recognition
import uuid

app = Flask(__name__)
CORS(app)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
KNOWN_FOLDER = '{}/known/'.format(PROJECT_HOME)
UNKNOWN_FOLDER = '{}/unknown/'.format(PROJECT_HOME)
app.config['KNOWN_FOLDER'] = KNOWN_FOLDER
app.config['UNKNOWN_FOLDER'] = UNKNOWN_FOLDER


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/', methods = ['POST'])
def api_root():
	app.logger.info(PROJECT_HOME)
	if request.method == 'POST':
		app.logger.info(app.config['KNOWN_FOLDER'])
		img_data = request.form['image']
		img_data = img_data.replace('data:image/jpeg;base64,', '')
		user_name = request.form['user']
		img_name = secure_filename(user_name + '.jpg')
		create_new_folder(app.config['KNOWN_FOLDER'])
		saved_path = os.path.join(app.config['KNOWN_FOLDER'], img_name)
		with open(saved_path, "wb") as fh:
    			fh.write(img_data.decode('base64'))
		app.logger.info("saving {}".format(saved_path))
		return "Successfully registered " + user_name + "'s face."
	else:
		return "Oops, Something went wrong!"

@app.route('/face', methods = ['POST'])
def api_face():
	app.logger.info(PROJECT_HOME)
	if request.method == 'POST':
		app.logger.info(app.config['UNKNOWN_FOLDER'])
		img_data = request.form['image']
		img_data = img_data.replace('data:image/jpeg;base64,', '')
		new_uuid = uuid.uuid4()
		user_name = str(new_uuid)
		img_name = secure_filename(user_name + '.jpg')
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
					return "Successfully verified. Welcome {}, How can we help?".format(os.path.splitext(filename)[0])
				else:
					continue
			else:
				continue
		return "No face match found."
	else:
		return "No image"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)