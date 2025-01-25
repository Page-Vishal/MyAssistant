
import os
import time
import speech_recognition as sr

from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs( api_key = os.getenv("ELEVENLABS_API_KEY") )

r= sr.Recognizer()
source = sr.Microphone()

mp3_file_path = "output.mp3"

def start_assistant():  
    with open(mp3_file_path, "rb") as f:
        audio_bytes = f.read()

    print("The audio is being played:\n")
    play(audio_bytes, notebook=False, use_ffmpeg=False)
    print("Playing Completed\n")


def callback(recognizer, audio):
    start_assistant()

def start_listening():
    
    with source as s:
        r.adjust_for_ambient_noise(s, duration=2)
    
    # Start background listening
    print("Listening... CTRL+C ko stop")
    r.listen_in_background(source, callback)

    while True:
        time.sleep(.5)

start_listening()