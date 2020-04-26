

import flask
import os
import cv2
from flask import Flask , render_template , request , send_file , send_from_directory

UPLOAD_FOLDER = '/images/blur_img'

classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

upload_folder = 'images/'
ALLOWED_EXT = set(['pdf' , 'jpg' , 'jpeg' , 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

name = ''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/success' , methods = ['POST'])
def success():
	if request.method == 'POST':
		file = request.files['file']
		target = os.path.join(os.getcwd() , 'images')
		if file and allowed_file(file.filename):
			file.save(os.path.join(target , 'img' , file.filename))
			img = cv2.imread(os.path.join(target , 'img' , file.filename))
			gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
			faces = classifier.detectMultiScale(gray , 1.1 , 4)
			for (x, y, w, h) in faces:
				img[y:y+h , x:x+w] = cv2.blur(img[y:y+h , x:x+w], (90, 90) , 50)
				# cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
				# sub_face = img[y:y+h ,x:x+w]
				# sub_face = cv2.GaussianBlur(sub_face,(99,99), 50)
				# result_image[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face
			    
			new_target = os.path.join(target , 'blur_img')
			name = file.filename
			cv2.imwrite(os.path.join(new_target , file.filename), img)
			
			return render_template("success.html" , name = file.filename)

@app.route('/get_image/<filename>')
def get_image(filename):
	# return send_from_directory(app.config['UPLOAD_FOLDER'] , filename)
	target = os.path.join(os.getcwd() , 'images')
	new_target = os.path.join(target , 'blur_img')
	name = os.path.join(new_target , filename)
	return send_file(name)
	# if request.method == 'POST':
	# 	target = os.path.join(os.getcwd() , 'images')
	# 	new_target = os.path.join(os.getcwd() , 'blur_img')
		
@app.route('/use')
def use():
	return render_template("use.html")



if __name__ == "__main__":
	app.run(debug = True)