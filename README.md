# AI-Powered Document Analysis & Extraction API

## Description

Intelligent document processing system that extracts, analyses, and summarises content from PDF, DOCX, and image files.

## Tech Stack

- Framework: FastAPI (Python)
- PDF Extraction: PyMuPDF
- DOCX Extraction: python-docx
- OCR: Tesseract via pytesseract
- AI Model: Anthropic Claude (claude-sonnet-4-20250514)
- Deployment: Docker on Render

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your API keys
4. Run: `uvicorn src.main:app --host 0.0.0.0 --port 8000`

## API Endpoint

POST /api/document-analyze
Header: x-api-key: your_key

## Approach

- PDF: PyMuPDF extracts text page by page
- DOCX: python-docx reads paragraphs and tables
- Image: Tesseract OCR extracts text
- Claude API handles summary, entity extraction, and sentiment in one prompt
