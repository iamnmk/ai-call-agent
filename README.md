# Sollvr Voice Assistant

A voice assistant application built with FastAPI, OpenAI, and Twilio.

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
   OPENAI_API_KEY=your_openai_api_key_here
   TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
   TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
   ```

## Running the Application

Start the server with:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## Project Structure

```
sollvr-voice-assistant/
│
├── app.py                     # Main FastAPI application
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this file)
│
├── static/                    # Static folder for audio files
│   └── (generated mp3 files)
│
└── README.md                  # This documentation
```

## API Endpoints

- `GET /`: Welcome message
- Additional endpoints will be documented here as they are implemented 