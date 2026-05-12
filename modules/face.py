import os
import cv2 as camera
import face_recognition 
from PIL import Image
import numpy as np
import time
from actions import system_actions

def test_webcam():
    raw_img = Image.open("Viko_image.jpeg").convert("RGB") #open the refrence photo and convdert to RGB removing every other detail
    viko_img = np.array(raw_img) #convert picture into grid of numbers
    viko_enc = face_recognition.face_encodings(viko_img)[0] #so hog model mathematically defines your face and create 128 unique number 
    
    stranger_timer = None
    target_app = "NotePad"
    cam = camera.VideoCapture(0) #starts your laptop camera

    while True:
        ret, frame = cam.read() #grabs a single frame from the video for detection 
        if not ret: break
        
        resized_frame = camera.resize(frame, (0, 0), fx=0.5, fy=0.5) #resizing the image for faster calculation less pixel 
        rgb_frame = camera.cvtColor(resized_frame, camera.COLOR_BGR2RGB) # using hog model which uses RGB hence converting frame from BGR(used in opencv)
        
        # in these 2 line we take the frame from viedo and then create a unique 128 number and then compare those 2 number to check if face matches or not 
        face_locations = face_recognition.face_locations(rgb_frame, model="hog") 
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        stranger_frame = False

        for (top, right, bottom, left), face_enc in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces([viko_enc], face_enc)
            
            if True in matches:
                name = "Viko"
                stranger_timer = None
            else:
                name = "Stranger"
                stranger_frame = True

            # Draw rectangle inside the loop so 'left', 'top', etc. are always defined
            camera.rectangle(resized_frame, (left, top), (right, bottom), (0, 255, 0), 2)
            camera.putText(resized_frame, name, (left, top - 10), camera.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if stranger_frame:
            if stranger_timer is None:
                stranger_timer = time.time() # Start the clock
            else:
                elapsed_time = time.time() - stranger_timer
                if elapsed_time > 3:
                    system_actions.close_app(target_app)
                    stranger_timer = None # Reset after closing
        else:
            stranger_timer = None # Reset if no face is seen at all

        camera.imshow('WhoThere Webcam Test', resized_frame)

        if camera.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    camera.destroyAllWindows()

if __name__ == "__main__":
    test_webcam()