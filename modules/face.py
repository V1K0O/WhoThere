import os
import cv2 as camera
import face_recognition 
from PIL import Image
import numpy as np

def test_webcam():
    raw_img = Image.open("Viko_image.jpeg").convert("RGB")
    viko_img = np.array(raw_img)
    viko_enc = face_recognition.face_encodings(viko_img)[0]
    
    cam = camera.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret: break
        
        resized_frame = camera.resize(frame, (0, 0), fx=0.5, fy=0.5) #resizing the image for faster calculation less pixel 
        rgb_frame = camera.cvtColor(resized_frame, camera.COLOR_BGR2RGB) # using hog model which uses RGB hence converting frame from BGR

        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_enc in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces([viko_enc], face_enc)
            name = "Unknown"

            if True in matches:
                name = "Viko"
                print("Match found!")

            camera.rectangle(resized_frame, (left, top), (right, bottom), (0, 255, 0), 2)
            camera.putText(resized_frame, name, (left, top - 10), camera.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        camera.imshow('WhoThere Webcam Test', resized_frame)

        if camera.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    camera.destroyAllWindows()

if __name__ == "__main__":
    test_webcam()