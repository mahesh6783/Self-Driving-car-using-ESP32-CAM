import speech_recognition as sr
import pyautogui

import urllib.request
import time
 
# repace ip
url = ""


def sendRequest(url):
    a = urllib.request.urlopen(url)


def listen_to_voice_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print(f"Command: {command}")
        print(command)
        return command
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None


def execute_command(command):
    if "forward" in command:
        print("Moving Forward...")
        sendRequest(url+"/action?go=forward")
        time.sleep(3)
        sendRequest(url + "/action?go=stop")
        # sendRequest(url+"/action?go=forward")
        # sendRequest(url+"/action?go=stop")

    elif "backward" in command:
        print("Moving Backward...")
        sendRequest(url+"/action?go=backward")
        time.sleep(3)
        sendRequest(url + "/action?go=stop")


    elif "left" in command:
        print("Moving Left...")
        sendRequest(url+"/action?go=left")
        time.sleep(1)
        sendRequest(url+"/action?go=stop")


    elif "right" in command:
        print("Moving Right...")

        sendRequest(url+"/action?go=right")
        time.sleep(1)
        sendRequest(url + "/action?go=stop")
        # sendRequest(url+"/action?go=stop")
    elif "r i g h t" in command:
        print("Moving Right...")

        sendRequest(url+"/action?go=right")
        time.sleep(1)
        sendRequest(url + "/action?go=stop")

    elif "stop" in command:
        print("Stopping...")
        # Assuming space key stops the movement
        sendRequest(url + "/action?go=stop")
    elif "exit" in command:
        print("Exiting program...")
        exit()
    else:
        print(command)
        print("Command not recognized. Please try again.")


if __name__ == "__main__":
    while True:
        voice_command = listen_to_voice_command()
        if voice_command:
            execute_command(voice_command)
