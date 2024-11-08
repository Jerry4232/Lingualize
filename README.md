# Lingualize - Real-time Speech-to-Text and Text-to-Speech Assistant

Lingualize is a Python-based real-time speech-to-text and text-to-speech application that connects multiple APIs for seamless conversation flow. It listens to your voice, transcribes the speech to text, generates a response from OpenAI's GPT, and then converts the response back into speech.

## Prerequisites

- Install the required Python packages (`requests`, `pydub`, etc.) using `pip`.
- You will need API keys for **OpenAI (GPT-3/ChatGPT)**, **AssemblyAI**, and **ElevenLabs** for speech generation.
  
## Getting Started

### 1. **Create a `.env` File**

First, create a `.env` file in the `lingualize` folder (where your project files are located).

### 2. **Set Up API Keys**

Open the `.env` file and add the following lines with your own API keys:

```env
GPT_API_KEY=your_openai_api_key
ASSEMBLY_API_KEY=your_assemblyai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

### Step 2: Install Dependencies

**Install Python Packages**

Ensure you have the required Python packages installed. You can install them using the command below:

```
pip install -r requirements.txt
```

**Install FFmpeg**

Lingualize relies on FFmpeg for handling audio streams. Download FFmpeg from [https://www.ffmpeg.org/](https://www.ffmpeg.org/), and install it on your machine.

After installation, add FFmpeg to your system's `PATH` variable:

- **Windows**: Add the FFmpeg `bin` directory to the system PATH through Environment Variables in System Properties.

- **Mac/Linux**: Add FFmpeg to your PATH by editing `.bashrc`, `.zshrc`, or equivalent, and adding: 

  ```bash     export PATH="/path/to/ffmpeg/bin:$PATH"     ```

### Step 3: Run the Application

Start the application by running the following command:

```
python main.py
```

If everything is set up correctly, you should see the following output in the console:

```
Successfully Connected!
Press Ctrl+C to stop recording.
```

### Step 4: Start Interacting

1. **Speak**: Speak in **English** into your microphone.
2. **Transcription**: The application will detect your speech and display it in the console as:

```
User: <your spoken text>
```

**Response Generation**: The application will process the transcription and respond using GPT, displaying the response as:

1. ```
   output get!
   AI: <GPT response text>
   ```

2. **Audio Playback**: The generated response from GPT will be converted to audio using ElevenLabs and played through your speakers.

3. **Example:**![example test](C:/Users/Jerry/Desktop/example test2.png)![example test2](assets/example test2.png)

### Changing the Voice

You can change the voice used for the text-to-speech output by modifying the `ELEVENLABS_VOICE_ID` variable in the code with the desired voice ID. For available voice models, refer to the ElevenLabs API documentation.

## Example `.env` File

```
# .env file
GPT_API_KEY=your_openai_api_key
ASSEMBLY_API_KEY=your_assemblyai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

## Dependencies

The following libraries are required for Lingualize to work correctly:

- `requests` - For making HTTP requests to API endpoints.
- `pydub` - For handling audio playback.
- `assemblyai` - For real-time transcription services.
- `openai` - For generating responses from GPT.
- `elevenlabs` - For generating speech from text.

You can install these dependencies by running:

```
pip install -r requirements.txt
```

## Troubleshooting

- **No Response or Error Generating Audio**: Ensure your API keys are correctly configured and the `.env` file is in the correct directory.
- **Voice Not Playing**: Verify that your audio playback system (e.g., speakers or headphones) is functioning and properly connected.
- **Console Messages**: Watch the console for prompts like `Successfully Connected!` and `Press Ctrl+C to stop recording` to ensure the program is running as expected.

## License

This project is open-source and available under the MIT License.

## Contributions

Contributions are welcome! Feel free to open a pull request or issue if you find bugs or would like to improve the project.