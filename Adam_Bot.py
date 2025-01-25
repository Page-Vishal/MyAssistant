'Notice Board'

#####
# Needs call back function
# Needs memory

# audio chunking and streaming, Malai aaudaina
# Threading for faster but bored 
#####

import os
from dotenv import load_dotenv
from groq import Groq
import speech_recognition as sr
import pyaudio
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs

load_dotenv()
groq_client = Groq(api_key = os.getenv("GROQ_API_KEY"))
llm_client = Groq(api_key = os.getenv("GROQ_API_KEY"))
elabs_client = ElevenLabs( api_key = os.getenv("ELEVENLABS_API_KEY") )

# Function to capture audio
def capture_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Please speak into the microphone...\n")
        audio_data = recognizer.listen(source)
        print("Audio captured!")
    return audio_data

# Save audio to a WAV file
def save_audio_to_wav(audio_data, output_file="AudioIn/microphone_input.wav"):
    with open(output_file, "wb") as file:
        file.write(audio_data.get_wav_data())
    return output_file

# Transcribe the audio
def model_transcribe(filename) :
    with open(filename, "rb") as file:
        transcription = groq_client.audio.transcriptions.create(
        file=(filename, file.read()),
        model="whisper-large-v3",
        response_format="verbose_json",
    )
    return transcription.text

#Use LLM to generate response
def response_generator(prompt):
    chat_completion = llm_client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {
                "role": "system",
                "content": "Your name is Adam Sawyer. You are a mildly talking assistant. You only provide a decently brief response neither too long nor too short."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    response = chat_completion.choices[0].message.content
    clean_response = response.replace("\n\n", " ")
    return clean_response

#Play the response back
def play_back(text) :
    audio = elabs_client.generate(
    text= text,
    voice=  "Adam",
    model="eleven_multilingual_v2",
    )
    return audio

#start the assistant
def start_assistant():
    # Capture, save, and transcribe audio
    audio_data = capture_audio()                    #returns audio data
    wav_file = save_audio_to_wav(audio_data)        #creates a microphone's input file as .wav
    prompt = model_transcribe(wav_file)             #returns the trasncribed text  

    response = response_generator(prompt)           #returns the response of the user's prompt

    return prompt,response

#The prompt,response feeding system
prompt,response = start_assistant()
#Printing both resposne
print(f'\nUSER: {prompt}')
print(f'\nADAM: {response}')

voice = play_back(response)                     #returns the audio of the assistant

play(voice, notebook=False, use_ffmpeg=False)   #play the audio

'''
audio_settings = Voice( voice_id="pNInz6obpgDQGcFmaJgB", 
                        settings=VoiceSettings(
                            stability=0.7,
                            similarity_boost=0.5,
                            style=0.0,
                            use_speaker_boost=True) 
                        )
'''
