import os
import speech_recognition as voice


r=voice.Recognizer() #listen to audio

with voice.Microphone() as source: #open system default microphone
    print("Calibrating for background noise...")
    r.adjust_for_ambient_noise(source, duration=0.5)
    print("Listening for 5 seconds...")
    # 2. Capture the audio
    audio = r.listen(source,timeout=None,phrase_time_limit=3) #tells system to listen



try:

    text = r.recognize_google(audio)
    print(f"You said: {text}")
    if "test" in text:
        os.system("start notepad")
except:
    print("Sorry, could not understand.")