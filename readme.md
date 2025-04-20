# E-Grading Handwritten Notes with OpenCV and Python

This project aims to automate the grading of handwritten answers using Optical Character Recognition (OCR) and image processing techniques. It allows educators to upload scanned images of handwritten answer sheets, process them to extract the text, compare them with a pre-uploaded answer key, and generate a score along with feedback.

## Features

- **Upload Handwritten Answer Sheets**: Users can upload scanned images of handwritten answer sheets.
- **OCR Text Extraction**: The system uses EasyOCR to extract text from the images.
- **Answer Grading**: Compares extracted text against a predefined answer key to grade answers.
- **Feedback Generation**: Displays feedback for each question, indicating correct or incorrect answers.
- **Answer Key Upload**: Educators can upload an answer key in a `.txt` format.
- **Real-Time Grading**: Provides real-time feedback and grading once the answer sheet is processed.

## Technologies Used

- **Flask**: For building the web application.
- **OpenCV**: For image preprocessing, including resizing, deskewing, denoising, and thresholding.
- **EasyOCR**: To perform Optical Character Recognition (OCR) on scanned handwritten answers.
- **Python**: For backend processing.
- **HTML/CSS**: For the user interface.

## Installation

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/e-grading-handwritten-notes.git
