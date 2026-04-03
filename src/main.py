import os
import base64
import logging
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.analyzer import analyze_document_bytes, extract_text, analyze_with_gemini

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Document Analysis API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key Security
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


class DocumentRequest(BaseModel):
    fileName: str
    fileType: str
    fileBase64: str


def verify_api_key(api_key: str = Security(api_key_header)):
    API_KEY = os.environ.get("API_KEY", "sk_track2_987654321")
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key


@app.get("/")
def root():
    return {"status": "ok", "message": "AI Document Analysis API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/document-analyze")
async def analyze_document(
    request: DocumentRequest,
    api_key: str = Depends(verify_api_key)
):
    file_type = request.fileType.lower().strip()

    if file_type not in ["pdf", "docx", "image"]:
        raise HTTPException(status_code=400, detail="Use pdf, docx, or image")

    try:
        file_bytes = base64.b64decode(request.fileBase64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 file")

    try:
        result = await analyze_document_bytes(file_bytes, request.fileName, file_type)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"AI error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

    # Keep API response shape stable (don’t include extractedText by default).
    result.pop("extractedText", None)
    return result