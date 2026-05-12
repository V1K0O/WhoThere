import os

def close_app(app_name):
    # This command forcefully closes the app by its name (e.g., "notepad.exe")
    # /F means force, /IM means image name
    print(f"Stranger Danger! Closing {app_name}...")
    os.system(f"taskkill /F /IM {app_name}.exe /T")