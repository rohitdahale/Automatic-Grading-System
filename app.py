from flask import Flask, render_template, request
import os
from config import UPLOAD_FOLDER
from ocr_utils import preprocess_image, extract_text, grade_answers, load_model_answers, save_model_answers_from_txt
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    feedback = None
    if request.method == 'POST':
        file = request.files['sheet']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            processed = preprocess_image(filepath)
            cv2.imwrite(filepath, processed)

            extracted_text = extract_text(filepath)

            if not os.path.exists("model_answers.json"):
                return "Please upload answer key first at /upload-answer-key"

            model_answers = load_model_answers()
            score, total, feedback = grade_answers(extracted_text, model_answers)

            return render_template('index.html', score=score, total=total, feedback=feedback, image=file.filename)
    return render_template('index.html')

@app.route('/upload-answer-key', methods=['GET', 'POST'])
def upload_answer_key():
    if request.method == 'POST':
        file = request.files['keyfile']
        if file and file.filename.endswith('.txt'):
            content = file.read().decode('utf-8').splitlines()
            save_model_answers_from_txt(content)
            return render_template("upload_answer_key.html", success=True)
    return render_template("upload_answer_key.html", success=False)

if __name__ == '__main__':
    app.run(debug=True)
