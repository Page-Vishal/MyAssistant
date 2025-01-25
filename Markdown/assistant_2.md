# AI Voice Assistant Becca

## Becca Hale

Becca Hale is an AI-powered voice assistant designed for interactive conversations. Below is a detailed explanation of her features, setup, and working mechanism.

---

## About Becca Hale

- **User**:      `Vishal Sigdel`
- **Assistant**: `Becca Hale`

Becca is an AI-powered assistant designed to simulate a natural back-and-forth conversation. She is modeled as an engineering student pursuing a Bachelor of Engineering in Electronics, Communication, and Information.

While Becca can hold coherent conversations, she currently lacks memory functionality.

---

### Key Features

1. **Speech-to-Text (STT)**: Powered by Groq "whisper-large-v3."
2. **Response Generation**: Utilizes Groq "gemma2-9b-it" as the Large Language Model (LLM).
3. **Text-to-Speech (TTS)**: Employs "eleven_multilingual_v2" for voice synthesis.
   - **Voice**: Provided by "Serena" of ElevenLabs.

> **Note**: You can change the user’s name in the system prompt or adjust the printed name in the callback function.

---

## Technical Details

### Setup

- **Global Scope**:
  1. Import necessary libraries.
  2. Load environment variables containing API keys (Groq and ElevenLabs).
  3. Initialize `Recognizer` and `Microphone` instances at the start as we access it immediately. It doesnot need to initialized in global scope.

### Working

#### Step-by-Step Explanation

1. **Starting the Program**
   - The `start_listening` function initializes the process by:
     1. Adjusting the microphone for ambient noise.
     2. Calling the `listen_in_background` function with `source` and `callback` as parameters.
     3. Detecting sound via the `source`, which triggers the `callback` function.

   - **Loop for Continuity**:  
   There is looping function as:
     ```python
     while True:
         time.sleep(0.5)
     ```
     - **Purpose**:
       - Keeps the program running without exiting.
       - Reduces CPU usage by introducing a short delay in each iteration.

2. **Callback Function**
   - The `callback` function:
     - Accepts `recognizer` and `audio` inputs from `listen_in_background`.
     - Calls the `start_assistant` function, passing the `audio` parameter.

3. **Audio Processing**
   - Unlike previous versions with a separate capture function, the audio is directly passed to a function that:
     1. Saves the audio as a `.wav` file.
     2. Transcribes the audio file to generate a `prompt`.
     3. Generates a response using the LLM.

4. **Text and Voice Output**
   - The `callback` function:
     - Prints the conversation (both prompt and response).
     - Generates the response's voice using TTS and plays it back.

5. **Loop Back**
   - Once the response is played, the program returns to `listen_in_background`, awaiting new audio input.

---

### Summary

Becca Hale's workflow is streamlined to offer efficient and interactive voice assistant capabilities. The integration of Groq models and ElevenLabs ensures high-quality responses and speech synthesis, while the callback-driven approach facilitates continuous, real-time interaction.