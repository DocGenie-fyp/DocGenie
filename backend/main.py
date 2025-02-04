from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import whisper
import logging
from pydantic import BaseModel
from utils.report_generator import generate_medical_report_with_gpt  # Make sure this exists

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_FILE_TYPES = {"audio/wav", "audio/mpeg"}  # Add more MIME types if needed
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# Load Whisper Model
model = whisper.load_model("base")  # You can use "small", "medium", or "large" for better accuracy

class TranscriptionResponse(BaseModel):
    filename: str
    transcription: str
    report: str  # Make sure to include the report in the response model

@app.get("/")
def read_root():
    return {"message": "Welcome to DocGenie Backend"}

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Validate file type
        if file.content_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid file type. Only audio files are allowed.")

        # Validate file size
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 50 MB.")

        # Save the file
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"File uploaded successfully: {file.filename}")
        return {"filename": file.filename, "message": "File uploaded successfully"}

    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe/", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...), role: str = Header(default="doctor")):
    try:
        # Validate file type
        if file.content_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid file type. Only audio files are allowed.")

        # Validate file size
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 50 MB.")

        # Save the file
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        logger.info(f"Saving file to: {file_location}")
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Verify the file exists
        if not os.path.exists(file_location):
            raise HTTPException(status_code=500, detail="File was not saved correctly.")

        # Transcribe audio using Whisper
        logger.info(f"Transcribing file: {file_location}")
        result = model.transcribe(file_location)
        transcription = result["text"]

        # Generate a medical report using GPT
        logger.info(f"Generating medical report for the transcription")
        report = generate_medical_report_with_gpt(transcription, role)

        logger.info(f"Transcription and report generation completed for file: {file.filename}")
        return {
            "filename": file.filename,
            "transcription": transcription,
            "report": report  # Include the generated report in the response
        }

    except Exception as e:
        logger.error(f"Error transcribing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
