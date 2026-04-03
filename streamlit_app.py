import json
import os
import base64
import requests
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from src.analyzer import detect_file_type

load_dotenv(override=False)

st.set_page_config(page_title="Doc Analyzer", page_icon="📄", layout="wide")

APP_CSS = """
<style>
  .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1200px; }
  .da-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 14px 16px;
  }
  .da-muted { opacity: 0.8; }
  .da-kv { display:flex; gap:12px; flex-wrap: wrap; }
  .da-kv > div { padding: 10px 12px; border-radius: 12px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.06); }
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)

st.markdown(
    """
<div class="da-card">
  <div style="display:flex; align-items:baseline; justify-content:space-between; gap: 16px;">
    <div>
      <div style="font-size: 28px; font-weight: 700;">AI Document Analyzer</div>
      <div class="da-muted">Upload a PDF/DOCX/Image → extract text → summary + entities + sentiment (Gemini)</div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

RAILWAY_URL = "https://doc-analyzer-production-1e83.up.railway.app"
API_KEY = "sk_track2_987654321"

with st.sidebar:
    st.header("Settings")
    st.checkbox("Show extracted text", value=False, key="show_text")

uploaded = st.file_uploader(
    "Upload a document",
    type=["pdf", "docx", "png", "jpg", "jpeg", "webp", "bmp", "tif", "tiff"],
)

col_a, col_b, col_c = st.columns([1, 1, 2])
with col_a:
    override_type = st.selectbox("File type", options=["auto", "pdf", "docx", "image"], index=0)
with col_b:
    run = st.button("Analyze", type="primary", disabled=uploaded is None)
with col_c:
    st.caption("Tip: For scanned PDFs, OCR accuracy may be better if you upload the image pages.")


if run and uploaded is not None:

    file_name = uploaded.name
    file_bytes = uploaded.getvalue()

    file_type = override_type
    if file_type == "auto":
        file_type = detect_file_type(file_name)

    if file_type not in ("pdf", "docx", "image"):
        st.error("Could not detect file type. Please choose PDF / DOCX / Image from the dropdown.")
        st.stop()

    with st.spinner("Extracting text and running AI analysis…"):
        try:
            endpoint = f"{RAILWAY_URL}/api/document-analyze"
            headers = {"x-api-key": API_KEY}
            payload = {
                "fileName": file_name,
                "fileType": file_type,
                "fileBase64": base64.b64encode(file_bytes).decode()
            }
            response = requests.post(endpoint, json=payload, headers=headers, timeout=120)

            if response.status_code == 401:
                st.error("Invalid API key. Check your Railway environment variables.")
                st.stop()
            elif response.status_code == 400:
                st.error(f"Bad request: {response.text}")
                st.stop()
            elif response.status_code != 200:
                st.error(f"API error {response.status_code}: {response.text}")
                st.stop()

            result = response.json()

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to Railway API. Check if your Railway service is running.")
            st.stop()
        except requests.exceptions.Timeout:
            st.error("Request timed out. The document may be too large or the server is busy.")
            st.stop()
        except Exception as e:
            st.error(str(e))
            st.stop()

    st.success("Analysis complete.")

    top_left, top_right = st.columns([3, 1])
    with top_left:
        st.subheader("Summary")
        st.write(result.get("summary", ""))
    with top_right:
        st.subheader("Sentiment")
        st.markdown(
            f"""
<div class="da-kv">
  <div><div class="da-muted">File</div><div style="font-weight:600">{file_name}</div></div>
  <div><div class="da-muted">Type</div><div style="font-weight:600">{file_type.upper()}</div></div>
  <div><div class="da-muted">Sentiment</div><div style="font-weight:700">{result.get("sentiment", "Neutral")}</div></div>
</div>
""",
            unsafe_allow_html=True,
        )

    tab_entities, tab_text, tab_json = st.tabs(["Entities", "Extracted text", "Raw JSON"])

    with tab_entities:
        entities = result.get("entities") or {}
        e1, e2, e3, e4, e5 = st.columns(5)
        with e1:
            st.caption("Names")
            st.write(entities.get("names", []))
        with e2:
            st.caption("Dates")
            st.write(entities.get("dates", []))
        with e3:
            st.caption("Organizations")
            st.write(entities.get("organizations", []))
        with e4:
            st.caption("Amounts")
            st.write(entities.get("amounts", []))
        with e5:
            st.caption("Locations")
            st.write(entities.get("locations", []))

    with tab_text:
        if st.session_state.get("show_text"):
            st.text_area("Text", value=result.get("extractedText", ""), height=360)
        else:
            st.info("Enable **Show extracted text** in the sidebar to view the extracted text.")

    with tab_json:
        st.json(result)

    export = dict(result)
    export["analyzedAt"] = datetime.utcnow().isoformat() + "Z"
    export_json = json.dumps(export, indent=2, ensure_ascii=False).encode("utf-8")

    st.download_button(
        "Download JSON",
        data=export_json,
        file_name=f"{os.path.splitext(file_name)[0]}_analysis.json",
        mime="application/json",
    )