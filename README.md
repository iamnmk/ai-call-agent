# Sollvr Voice Assistant

A voice assistant application built with FastAPI, OpenAI, Deepgram, ElevenLabs, and Twilio.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with the following variables:
   ```
   # OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Deepgram API Key for speech-to-text
   DEEPGRAM_API_KEY=your_deepgram_api_key_here
   
   # ElevenLabs API Key and Voice ID for text-to-speech
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ELEVENLABS_VOICE_ID=your_voice_id_here
   
   # Base URL for the application (used for audio file URLs)
   # For local development: http://localhost:8000
   # For production: https://your-app-name.railway.app
   BASE_URL=http://localhost:8000
   ```

## Running the Application Locally

Start the server with:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## Docker Deployment

### Building the Docker Image
```bash
docker build -t sollvr-voice-assistant .
```

### Running the Container
```bash
docker run -p 8000:8000 --env-file .env sollvr-voice-assistant
```

## Railway Deployment

1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Initialize your project:
   ```bash
   railway init
   ```

4. Add your environment variables in the Railway dashboard or using the CLI:
   ```bash
   railway variables set OPENAI_API_KEY=your_key
   railway variables set DEEPGRAM_API_KEY=your_key
   railway variables set ELEVENLABS_API_KEY=your_key
   railway variables set ELEVENLABS_VOICE_ID=your_voice_id
   railway variables set BASE_URL=your_railway_app_url
   ```

5. Deploy your application:
   ```bash
   railway up
   ```

## Twilio Configuration

1. Set up a Twilio account and purchase a phone number
2. Configure your Twilio phone number's Voice webhook:
   - Set the webhook URL to `https://your-app-url.railway.app/voice`
   - Make sure both GET and POST methods are accepted
3. Test the integration by calling your Twilio phone number

## Project Structure

```
sollvr-voice-assistant/
│
├── app.py                     # Main FastAPI application
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this file)
├── Dockerfile                 # Docker configuration
├── .dockerignore              # Docker ignore file
│
├── static/                    # Static folder for audio files
│   └── (generated mp3 files)
│
└── README.md                  # This documentation
```

## API Endpoints

- `GET /`: Health check endpoint
- `GET/POST /voice`: Entry point for Twilio voice calls
- `GET/POST /process_audio`: Processes audio recording from Twilio 