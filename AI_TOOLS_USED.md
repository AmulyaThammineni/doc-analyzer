# AI Tools Used Documentation

## Project: AI-Powered Document Analysis & Extraction

## Hackathon: GUVI Hackathon 2026 — Track 2---

## 1. AI Tools Used During Development

### Claude (Anthropic)

- **Purpose:** Development assistance
- **How it was used:**
  - Helped understand FastAPI project structure and best practices
  - Assisted in debugging specific errors such as environment variable loading issues and Railway deployment configuration
  - Provided suggestions on architecture design and API response format
- **Extent of use:** Moderate — used for specific guidance and debugging

### ChatGPT (OpenAI)

- **Purpose:** Debugging assistance
- **How it was used:**
  - Helped investigate the 403 Forbidden error from the Gemini API
  - Provided information on Gemini model availability and correct model names
- **Extent of use:** Low — used for specific troubleshooting only

---

## 2. AI APIs Used Inside the Project

### Google Gemini 2.5 Flash (via REST API)

- **Provider:** Google AI Studio
- **Purpose:** Core AI analysis engine
- **How it is used:**
  - Receives extracted text from documents
  - Generates a concise summary of the document content
  - Extracts named entities — names, dates, organizations, monetary amounts, locations
  - Classifies overall sentiment as Positive, Neutral, or Negative
- **Integration method:** Direct HTTP REST API call using `httpx`
- **Endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent`

### Tesseract OCR

- **Provider:** Open source (UB Mannheim build for Windows)
- **Purpose:** Text extraction from image files
- **How it is used:**
  - Converts image files (PNG, JPG, etc.) to extractable text
  - Uses `--psm 6` mode optimized for document-style text blocks
- **Integration method:** via `pytesseract` Python wrapper

---

## 3. What Was Built Independently

- Problem statement selection and solution approach
- Tech stack decisions (FastAPI, PyMuPDF, python-docx, Tesseract, Gemini)
- Core application logic — text extraction pipeline for PDF, DOCX, and image formats
- Gemini REST API integration using direct HTTP calls
- Testing with real documents across all three file formats
- Railway deployment setup including Docker configuration and environment variables
- GitHub repository management and version control

---

All AI tools used during development and within the application have been fully disclosed above. No AI-generated responses have been hardcoded into the application. The system dynamically processes every document using live AI inference at runtime.
