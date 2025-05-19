from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from twilio.twiml.voice_response import VoiceResponse
import openai
import requests
import os
import uuid
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "YOUR_VOICE_ID")  # Default to placeholder
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")  # Default to localhost for development

# Init app and static route
app = FastAPI(title="SOLLVR Voice Assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"status": "healthy", "message": "SOLLVR Voice Assistant API is running"}

@app.post("/voice")
async def handle_voice_call(request: Request):
    response = VoiceResponse()
    response.say("Hi, I'm Sam from SOLLVR. Please say something after the beep.")
    response.record(timeout=5, transcribe=False, max_length=10, action="/process_audio")
    return PlainTextResponse(str(response))

@app.post("/process_audio")
async def process_audio(request: Request, RecordingUrl: str = Form(...)):
    try:
        # Step 1: Download audio from Twilio
        audio_data = requests.get(RecordingUrl + ".wav").content

        # Step 2: Transcribe using Deepgram
        deepgram_response = requests.post(
            "https://api.deepgram.com/v1/listen",
            headers={"Authorization": f"Token {DEEPGRAM_API_KEY}"},
            data=audio_data
        )
        user_text = deepgram_response.json()["results"]["channels"][0]["alternatives"][0]["transcript"]

        # Step 3: ChatGPT response
        chat = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a smart, friendly, and professional AI voice agent working at SOLLVR, an IT services company.

Your job is to:
- Greet callers warmly
- Explain what SOLLVR does: building MVPs, apps, SaaS tools, and infrastructure planning
- Answer questions naturally
- Sound like a helpful expert, but never overly technical unless asked
- Collect lead information if appropriate
- Ask if the caller wants to be contacted by a real team member
- Be concise, polite, and natural like a real assistant

NEVER say you are an AI. Always speak as a human agent named 'Sam from SOLLVR.'
"""
                },
                {"role": "assistant", "content": "Hi! This is Sam from SOLLVR. How can I help you today?"},
                {"role": "user", "content": user_text}
            ]
        )
        ai_response = chat["choices"][0]["message"]["content"]

        # Step 4: TTS using ElevenLabs
        tts_response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": ai_response,
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
            }
        )

        # Step 5: Save as a unique file
        file_id = str(uuid.uuid4())
        filename = f"static/{file_id}.mp3"
        with open(filename, "wb") as f:
            f.write(tts_response.content)

        # Step 6: Return Twilio VoiceResponse
        response = VoiceResponse()
        response.play(f"{BASE_URL}/static/{file_id}.mp3")
        return PlainTextResponse(str(response))
    
    except Exception as e:
        # Log the error and return a friendly message
        print(f"Error processing audio: {str(e)}")
        response = VoiceResponse()
        response.say("I apologize, but I'm having trouble processing your request right now. Please try again later.")
        return PlainTextResponse(str(response))
