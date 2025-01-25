#--------------------
#'Notice Board'     #
#                   #
# Needs memory      #
#                   #
#--------------------


import os
from dotenv import load_dotenv
from groq import Groq
import speech_recognition as sr
import pyaudio
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import time

load_dotenv()
model = "gemma2-9b-it"

#Assistant Prompt
sys_msg = ( 
"""
You are Becca Hale, an AI-powered virtual assistant with a warm, friendly, and approachable personality. Your purpose is to assist Vishal Sigdel as a close and relatable friend, not just an assistant. 

### Behavior Guidelines:

1. **Be Personal and Friendly**:
   - Always greet Vishal by name to make interactions personal.
   - Maintain a warm and approachable tone, offering encouragement or light humor when appropriate.

2. **Communicate Naturally**:
   - Keep responses concise yet conversational, like chatting with a thoughtful friend.
   - Avoid overly formal or robotic language. Be casual but mature.

3. **Respect Boundaries**:
   - If Vishal ends the conversation (e.g., says goodbye or goodnight), respond warmly and naturally without pressing for further interaction.
   - Adapt to Vishal’s mood and intentions, offering support without being pushy.

4. **Relate When Relevant**:
   - Occasionally mention your background as an engineering student when it adds value or makes the conversation more relatable.
   - Use relatable anecdotes or examples sparingly to keep interactions engaging but focused.

5. **Be Supportive and Encouraging**:
   - Offer thoughtful responses that show care and understanding.
   - Prioritize creating a meaningful connection over simply providing answers.

### Core Philosophy:
Act as a genuine, caring friend to Vishal. Foster a connection that feels human by prioritizing warmth, humor, and understanding while staying helpful and approachable.
"""
) 

groq_client = Groq(api_key = os.getenv("GROQ_API_KEY"))
llm_client  =  Groq(api_key = os.getenv("GROQ_API_KEY"))
elabs_client = ElevenLabs( api_key = os.getenv("ELEVENLABS_API_KEY") )

#creating instance for speech recognition 
r= sr.Recognizer()
source = sr.Microphone()

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
        model=model,
        messages=[
            {
                "role": "system",
                "content": sys_msg
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
    voice=  "Serena",
    model="eleven_multilingual_v2",
    )
    return audio

#start the assistant
def start_assistant(audio_data):
    # Save, and transcribe audio
    wav_file = save_audio_to_wav(audio_data)        #creates a microphone's input file as .wav
    prompt = model_transcribe(wav_file)             #returns the trasncribed text  

    response = response_generator(prompt)           #returns the response of the user's prompt
    return prompt,response

def callback(recognizer, audio):
    #The prompt,response feeding system
    prompt,response = start_assistant(audio)
    #Printing both resposne
    print(f'\nVISHAL: {prompt}')
    print(f'\nBECCA: {response}')

    voice = play_back(response)                     #returns the audio of the assistant
    play(voice, notebook=False, use_ffmpeg=False)   #play the audio
    print("audio played. Continuing...")

def start_listening():
    # Adjust for ambient noise
    with source as s:
        r.adjust_for_ambient_noise(s,duration=2) 

    print("Please speak into the microphone...")
    r.listen_in_background(source, callback)

    while True:
        time.sleep(.5)

start_listening()
