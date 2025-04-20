import cv2
import numpy as np
import easyocr
import json
from config import UPLOAD_FOLDER

reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (1200, 1600))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Deskewing (optional)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = gray.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    denoised = cv2.fastNlMeansDenoising(deskewed, h=30)
    kernel = np.ones((1, 1), np.uint8)
    opened = cv2.morphologyEx(denoised, cv2.MORPH_OPEN, kernel)
    thresh = cv2.adaptiveThreshold(opened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 11)



    return thresh

def extract_text(image_path):
    result = reader.readtext(image_path, paragraph=True)
    full_text = " ".join([line[1] for line in result])
    return full_text

def grade_answers(text, model_answers):
    score = 0
    total = len(model_answers)
    feedback = []
    for question, correct_answer in model_answers.items():
        if correct_answer.lower() in text.lower():
            score += 1
            feedback.append((question, "✔️"))
        else:
            feedback.append((question, "❌"))
    return score, total, feedback

def load_model_answers():
    with open("model_answers.json", "r") as f:
        return json.load(f)

def save_model_answers_from_txt(txt_lines):
    model_answers = {}
    for line in txt_lines:
        if ":" in line:
            q, a = line.split(":", 1)
            model_answers[q.strip()] = a.strip()
    with open("model_answers.json", "w") as f:
        json.dump(model_answers, f, indent=4)
    return model_answers
