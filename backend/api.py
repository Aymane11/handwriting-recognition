import os
import base64
from flask import Flask, request
import time

app = Flask(__name__)



current_dir = os.path.dirname(os.path.realpath(__file__))

model_filename = "abc.h5"
model_path = os.path.join(current_dir, "models", model_filename)

UPLOAD_DIRECTORY = os.path.join(current_dir, "images")

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY

def current_milli_time():
    return round(time.time() * 1000)

def b64_to_image(imgstring):
    imgdata = base64.b64decode(imgstring, ' /')
    filename = os.path.join(UPLOAD_DIRECTORY,f'image{current_milli_time()}.jpg')
    with open(filename, 'wb') as f:
        f.write(imgdata)
    return filename


def model(model_path, image_path):
    # Read image from image_path
    # Run splitting
    # output = ''
    # For letter in splits : run model and add prediction to output - Remove letter image
    # Return output
    return "THIS IS A SIMPLE TEST"

@app.route('/predict', methods=['POST'])
def predict():
    imgB64 = request.args.get("image")
    filename = b64_to_image(imgB64)
    return model(model_path, filename)


if __name__ == '__main__':
    app.run(debug=True)
