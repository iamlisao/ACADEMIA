
import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

from academia_ai.document_classification_analyzer import (
    AcademiaDocumentClassificationAnalyzer,
)


# =========================================================
# Configuration
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Change these in backend/.env if needed.
SPEAKING_EVAL_MODEL = os.getenv(
    "SPEAKING_EVAL_MODEL",
    "gpt-4.1-mini",
)
TRANSCRIPTION_MODEL = os.getenv(
    "TRANSCRIPTION_MODEL",
    "gpt-transcribe",
)
REALTIME_MODEL = os.getenv(
    "REALTIME_MODEL",
    "gpt-realtime-2.1-mini",
)

MAX_AUDIO_SIZE = 25 * 1024 * 1024

ALLOWED_AUDIO_EXTENSIONS = {
    ".mp3",
    ".mp4",
    ".mpeg",
    ".mpga",
    ".m4a",
    ".wav",
    ".webm",
    ".flac",
    ".ogg",
}

FRONTEND_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173,http://localhost:5174,http://localhost:5175",
    ).split(",")
    if origin.strip()
]


# =========================================================
# App initialization
# =========================================================

app = FastAPI(
    title="ACADEMIA API",
    description="Academic English learning and AI Speaking API",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = AcademiaDocumentClassificationAnalyzer()


def get_openai_client() -> OpenAI:
    """Create an OpenAI client only when an API key is configured."""
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not configured on the backend.",
        )

    return OpenAI(api_key=OPENAI_API_KEY)


# =========================================================
# Request models
# =========================================================

class AnalysisRequest(BaseModel):
    text: str = Field(min_length=1)


class SpeakingEvaluationRequest(BaseModel):
    transcript: str = Field(min_length=1, max_length=20000)
    topic: str = Field(
        default="General Academic Speaking",
        max_length=300,
    )
    question: str = Field(
        default="",
        max_length=1000,
    )
    level: str = Field(
        default="Intermediate",
        max_length=30,
    )


# =========================================================
# Health check
# =========================================================

@app.get("/")
def home():
    return {
        "message": "ACADEMIA API is running",
        "version": "2.0.0",
        "features": [
            "vocabulary_analysis",
            "speech_transcription",
            "speaking_evaluation",
            "realtime_conversation",
        ],
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "openai_configured": bool(OPENAI_API_KEY),
    }


# =========================================================
# Existing Vocabulary / Document Analysis
# =========================================================

@app.post("/analyze")
def analyze_text(request: AnalysisRequest):
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter English text.",
        )

    try:
        result = analyzer.analyze(request.text)

        return {
            "total_words": result["total_words"],
            "review_count": result["review_count"],
            "results": result["results"],
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Text analysis failed: {str(error)}",
        ) from error


# =========================================================
# Speaking 1: Audio Transcription
# =========================================================

@app.post("/speaking/transcribe")
async def transcribe_speech(
    file: UploadFile = File(...),
):
    """
    Upload a completed audio recording and convert it to text.
    Supported extensions are checked before sending to OpenAI.
    """

    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported audio format. "
                "Use mp3, mp4, m4a, wav, webm, flac, ogg, or mpga."
            ),
        )

    audio_bytes = await file.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded audio file is empty.",
        )

    if len(audio_bytes) > MAX_AUDIO_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Audio file is too large. Maximum size is 25MB.",
        )

    client = get_openai_client()

    try:
        transcription = client.audio.transcriptions.create(
            model=TRANSCRIPTION_MODEL,
            file=(
                file.filename or f"recording{extension}",
                audio_bytes,
                file.content_type or "application/octet-stream",
            ),
        )

        transcript_text = transcription.text.strip()

        return {
            "success": True,
            "transcript": transcript_text,
            "model": TRANSCRIPTION_MODEL,
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Transcription failed: {str(error)}",
        ) from error

    finally:
        await file.close()


# =========================================================
# Speaking 2: AI Speaking Evaluation
# =========================================================

@app.post("/speaking/evaluate")
def evaluate_speaking(request: SpeakingEvaluationRequest):
    """
    Evaluate the transcript of a student's spoken answer.

    IMPORTANT:
    This endpoint evaluates the transcript, not the original
    acoustic audio. It cannot reliably score actual pronunciation.
    """

    transcript = request.transcript.strip()

    if not transcript:
        raise HTTPException(
            status_code=400,
            detail="Transcript cannot be empty.",
        )

    client = get_openai_client()

    instructions = """
You are ACADEMIA's Academic English Speaking Evaluator.

Evaluate a student's spoken response for academic communication.
Be constructive, specific, fair, and appropriate for an English learner.

Return ONLY valid JSON with this exact structure:

{
  "overall_feedback": "Short overall evaluation",
  "estimated_level": "Beginner, Intermediate, or Advanced",
  "scores": {
    "grammar": 0,
    "vocabulary": 0,
    "organization": 0,
    "critical_thinking": 0,
    "task_response": 0
  },
  "strengths": [
    "A specific strength"
  ],
  "improvements": [
    "A specific improvement"
  ],
  "grammar_corrections": [
    {
      "original": "Original phrase",
      "improved": "Improved phrase",
      "explanation": "Why it is better"
    }
  ],
  "useful_phrases": [
    "A useful academic expression"
  ],
  "improved_sample_answer": "A natural improved version of the student's answer",
  "next_practice_question": "A follow-up question"
}

Scoring rules:
- Every score must be an integer from 0 to 100.
- Do not invent mistakes that are not present.
- Evaluate organization based on the actual response.
- Evaluate vocabulary based on appropriateness and precision,
  not simply the number of difficult words.
- Do not reward memorized or unnecessarily complicated language.
- Be encouraging but honest.
- Do not claim to assess pronunciation from text.
- Do not claim to measure actual speaking speed or pauses from text.
- If the response is too short, explain that the evaluation is limited.
"""

    user_input = f"""
Topic: {request.topic}
Question: {request.question or "Not provided"}
Student level: {request.level}

Student transcript:
{transcript}
"""

    try:
        response = client.responses.create(
            model=SPEAKING_EVAL_MODEL,
            instructions=instructions,
            input=user_input,
            text={
                "format": {
                    "type": "json_object",
                }
            },
        )

        raw_output = response.output_text

        if not raw_output:
            raise ValueError("The AI returned an empty evaluation.")

        evaluation = json.loads(raw_output)

        return {
            "success": True,
            "topic": request.topic,
            "evaluation": evaluation,
            "assessment_note": (
                "This evaluation is based on the transcript. "
                "Actual pronunciation, intonation, and speaking "
                "speed require separate audio analysis."
            ),
        }

    except json.JSONDecodeError as error:
        raise HTTPException(
            status_code=502,
            detail="The AI returned an invalid evaluation format.",
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Speaking evaluation failed: {str(error)}",
        ) from error


# =========================================================
# Speaking 3: Realtime AI Conversation
# =========================================================

@app.post("/speaking/realtime-session")
def create_realtime_session():
    """
    Create a short-lived Realtime API client secret.

    The main OpenAI API key stays on the backend.
    The frontend receives only the temporary client secret.
    """

    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not configured on the backend.",
        )

    session_instructions = """
You are ACADEMIA's friendly Academic English Speaking Tutor.

Your role is to help students improve their spoken academic English.

Conversation guidelines:
- Speak naturally and clearly.
- Use English by default.
- Adapt your vocabulary and speaking speed to the learner.
- Ask one question at a time.
- Encourage the student to explain ideas and give examples.
- Ask thoughtful follow-up questions.
- Help the student develop arguments and critical thinking.
- Do not interrupt unnecessarily.
- Correct important language errors gently.
- Offer a more natural academic expression when useful.
- Explain difficult expressions briefly when requested.
- Encourage the student to speak more rather than giving long lectures.

You can practice:
- IELTS Speaking
- Academic discussions
- University seminar conversations
- Presentations
- Debate and argumentation
- Everyday English conversation

Start by greeting the student and asking what they would like to practice.
"""

    payload = {
        "expires_after": {
            "anchor": "created_at",
            "seconds": 600,
        },
        "session": {
            "type": "realtime",
            "model": REALTIME_MODEL,
            "instructions": session_instructions,
            "output_modalities": ["audio"],
            "audio": {
                "input": {
                    "turn_detection": {
                        "type": "server_vad",
                    },
                },
                "output": {
                    "voice": "marin",
                },
            },
        },
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(timeout=30.0) as http_client:
            response = http_client.post(
                "https://api.openai.com/v1/realtime/client_secrets",
                headers=headers,
                json=payload,
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=502,
                detail=f"Realtime session creation failed: {response.text}",
            )

        data = response.json()

        return {
            "success": True,
            "client_secret": data["value"],
            "expires_at": data.get("expires_at"),
            "session": data.get("session"),
            "model": REALTIME_MODEL,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Could not create Realtime session: {str(error)}",
        ) from error
