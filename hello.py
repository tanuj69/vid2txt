import os
import shutil
import cv2
from PIL import Image
import pytesseract
import numpy as np
from pytube import YouTube

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image_frames = 'image_frames'
prev_text = None # Initialize a variable to store the previous text

from pytube import YouTube

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        file_path = youtubeObject.download()
        new_file_name = 'balls.mp4'
        os.rename(file_path, new_file_name)
    except:
        print("An error has occurred")
    print("Download is completed successfully")

def create_folders():
    try:
        shutil.rmtree(image_frames)
    except OSError:
        pass
    if not os.path.exists(image_frames):
        os.makedirs(image_frames)
        return True
    return False

def process_video(src_vid):
    index = 0
    prev_frame = None
    while src_vid.isOpened():
        ret, frame = src_vid.read()
        if not ret:
            break
        # Convert frames to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_frame is not None:
            # Calculate the absolute difference between the current frame and the previous frame
            diff = cv2.absdiff(gray_frame, cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY))
            # Apply a threshold to the difference image
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            # Check if there are non-zero pixels in the threshold image
            if cv2.countNonZero(thresh) > 0:
                name = os.path.join(image_frames, f'frame_{index}.png')
                cv2.imwrite(name, frame)
                index += 1
                extract_text(name)
        prev_frame = frame
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    src_vid.release()
    cv2.destroyAllWindows()

def extract_text(image_path):
    global prev_text
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='eng')
        with open('output.txt', 'a', encoding='utf-8') as f:
            print(f'Text from {image_path}:')
            print(text)
            f.write(f'Text from {image_path}:\n{text}\n\n')
            prev_text = text
    except Exception as e:
        print(f'Error extracting text from {image_path}: {e}')

def process_images():
    if create_folders():
        src_vid = cv2.VideoCapture('abc.mp4')
        process_video(src_vid)

if __name__ == '__main__':
    process_images()
    #Download('https://www.youtube.com/shorts/8ndqjDGNw8k')