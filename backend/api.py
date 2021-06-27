import os
import shutil
import base64
import numpy as np
from PIL import Image
import tensorflow as tf
from datetime import datetime
from flask import Flask, request
from utils.extractor import extract_letters


app = Flask(__name__)


current_dir = os.path.dirname(os.path.realpath(__file__))

model_filename = "model.h5"

model_path = os.path.join(current_dir, "models", model_filename)
class_mapping = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt'

UPLOAD_DIRECTORY = os.path.join(current_dir, "images")
LETTERS_DIR = os.path.join(current_dir, "utils", "letters")

REMOVE_AFTER_PREDICTION = False

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY


def current_milli_time():
    return datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")



def b64_to_image(imgstring):
    imgdata = base64.b64decode(imgstring, ' /')
    filename = f'image_{current_milli_time()}.jpg'
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    with open(file_path, 'wb') as f:
        f.write(imgdata)
    return filename


def run_model(letter):
    # To run TF in CPU only
    with tf.device('/CPU:0'):
        model = tf.keras.models.load_model(model_path)
        letter_path = os.path.join(LETTERS_DIR, letter)
        image = Image.open(letter_path)
        image = image.convert('L')
        # convert image to numpy array
        data = np.asarray(image)
        # convert array to 28x28 array (matrix)
        # img = data.reshape([28, 28])
        data = data.reshape(1, 28, 28, 1)
        # normalize image
        d = data / 255.0
        # run prediction
        result_id = np.argmax(model.predict(d))
        prediction = class_mapping[result_id]
        return prediction


def get_text(filename, remove=False):
    # Run splitting
    extract_letters(filename)
    letters = os.listdir(LETTERS_DIR)
    # For letter in splits : run model and add prediction to output - Remove letter image
    output = ''.join(run_model(letter) for letter in letters)
    # Remove letters folder
    shutil.rmtree(LETTERS_DIR)
    if remove:
        # Remove image file if user wants to
        os.remove(os.path.join(UPLOAD_DIRECTORY, filename))
    # Return output
    return output


@app.route('/predict', methods=['POST'])
def predict():
    imgB64 = request.args.get("image")
    filename = b64_to_image(imgB64)
    return get_text(filename, remove=REMOVE_AFTER_PREDICTION)


if __name__ == '__main__':
    app.run(debug=False)
