import os
import tempfile
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav") -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=(filename, audio_file, "audio/wav"),
                response_format="text"
            )

        os.unlink(tmp_path)
        return transcription if isinstance(transcription, str) else transcription.text

    except Exception as e:
        return f"Error transcribing audio: {str(e)}"
