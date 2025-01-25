# AI Voice Assistant Adam

## Adam Sawyer

### Overview
This assistant is designed to perform Speech-to-Text (STT) and Text-to-Speech (TTS) operations, leveraging Groq's Whisper model for transcription and ElevenLabs for generating human-like voice responses. The architecture of the assistant is modular, with clearly defined functions for each step. Comments and function-based implementation ensure clarity and easy understanding.

---

### Key Features

1. **Speech-to-Text (STT)**: Powered by Groq "whisper-large-v3."
2. **Response Generation**: Utilizes Groq "gemma2-9b-it" as the Large Language Model (LLM).
3. **Text-to-Speech (TTS)**: Employs "eleven_multilingual_v2" for voice synthesis.
   - **Voice**: Provided by "Adam" of ElevenLabs.
---

## Features
1. **Audio Capture**: Listens to voice input from a microphone and processes it as binary data.
2. **Audio File Conversion**: Saves the captured audio as a `.wav` file.
3. **Speech-to-Text (STT)**: Transcribes the audio input into text using Groq's Whisper model.
4. **Response Generation**: Processes the user's transcribed input and generates a response using Groq's LLM (`gemma2-9b-it`).
5. **Text-to-Speech (TTS)**: Converts the response text into speech using ElevenLabs' TTS model (`eleven_multilingual_v2`) with the voice of Adam.
6. **Playback**: Plays the generated audio response directly.

---

## Workflow
The assistant’s functionality is divided into six main steps:

### 1. **Capture Audio**
- **Function**: `capture_audio`
- **Purpose**: Listens to audio from the microphone and processes it as binary data.
- **Returns**: `audio_data` (raw audio in bytes format).

### 2. **Save Audio to WAV**
- **Function**: `save_audio_to_wav`
- **Purpose**: Converts the binary audio input into a `.wav` file named `microphone_input.wav`. This file is required for transcription.
- **Returns**: `output_file` (saved `.wav` file).

### 3. **Speech-to-Text (STT)**
- **Function**: `model_transcribe`
- **Purpose**: Uses Groq’s Whisper model (`whisper-large-v3`) to transcribe the `.wav` file into text.
- **Process**: Opens the `.wav` file in binary mode (`rb`), processes the audio, and transcribes it.
- **Returns**: `text` (transcribed text from the user's voice input).

### 4. **Response Generation**
- **Function**: `response_generator`
- **Purpose**: Utilizes Groq’s LLM (`gemma2-9b-it`) to generate a response based on the transcribed text.
- **Features**:
  - Includes a system prompt for flexibility and tailored responses.
- **Returns**: `response` (response generated as a string).

### 5. **Playback**
- **Function**: `play_back`
- **Purpose**: Plays the generated response using ElevenLabs’ TTS model (`eleven_multilingual_v2` with Adam’s voice).
- **Returns**: Audio data as bytes, which is played back to the user.

### 6. **Start Assistant**
- **Function**: `start_assistant`
- **Purpose**: Orchestrates the entire process from capturing audio to playing back the response.
  - Captures audio and saves it as a `.wav` file.
  - Transcribes the audio into text.
  - Generates a response based on the transcription.
  - Converts the response into audio and plays it back.
- **Returns**:
  - `prompt`: The user’s input in text form.
  - `response`: The assistant’s response.

---

## Example Interaction
1. **User Input**: Speaks into the microphone.
2. **Assistant Process**:
   - Captures and saves the user’s voice as `microphone_input.wav`.
   - Transcribes the audio to text.
   - Generates a response to the user’s query.
   - Converts the response text into an audio file and plays it back.
3. **Output**:
   - Displays the user’s message and the assistant’s response.
   - Plays the audio response.

---

## Additional Customization
### Audio Settings
- The playback audio can be customized using ElevenLabs’ advanced audio settings. These settings can be modified as required to enhance the voice output.

---

## Notes
- Groq’s Whisper model (`whisper-large-v3`) was chosen for its transcription accuracy.
- ElevenLabs’ Adam voice (`eleven_multilingual_v2`) was used for its natural and human-like quality.
- The assistant is designed to balance simplicity and functionality, making it ideal for straightforward conversational AI use cases.

---