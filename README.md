# Pipecat Voice Chatbot

A real-time voice assistant built with [Pipecat](https://github.com/pipecat-ai/pipecat), FastAPI, and WebSockets.


##  Structure

```
voice-chatbot/
├── app/
│   ├── __init__.py
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── routes.py          # HTTP routes
│   │   └── websocket.py       # WebSocket handler
│   ├── core/                   # Core configuration
│   │   ├── __init__.py
│   │   └── config.py          # Settings and constants
│   ├── processors/             # Custom frame processors
│   │   ├── __init__.py
│   │   ├── audio_output.py    # Audio capture processor
│   │   └── end_call.py        # Call termination processor
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   └── bot.py             # Main bot pipeline
│   └── templates/              # Frontend templates
│       └── index.html         # Web interface
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 
└── README.md                  
```


### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add OpenAI and DeepGram API Keys**
   Edit `voice-chatbot\voice-chatbot\app\core\config.py` and add your API keys:
   ```
   DEEPGRAM_API_KEY: str = 'ADD_KEY_HERE'
   OPENAI_API_KEY: str = 'ADD_KEY_HERE'   
   ```

### Running the Application

```bash
python main.py
```

The server will start on `http://localhost:8000`

Open your browser and navigate to `http://localhost:8000` to start using the voice chatbot.

## Usage

1. Click the **"Start Call"** button to begin
2. Allow microphone access when prompted
3. Speak naturally with the AI assistant
4. The status indicator shows:
   -  **Green (Listening)**: Ready for your input
   -  **Pink (Bot Speaking)**: AI is responding
   -  **Gray (Not Connected)**: No active connection
5. Say "goodbye" or click **"Stop Call"** to end the conversation
6. Check logs in VS Code Console to see what has been transcribed 
