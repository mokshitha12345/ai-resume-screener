import streamlit as st
from sentence_transformers import SentenceTransformer, util
import PyPDF2
from docx import Document
from io import BytesIO
import pandas as pd
import time

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# UI Config
st.set_page_config(page_title="AI Resume Screener", page_icon="📋", layout="wide")

# CSS
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .result-card {
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

# Extractors
def extract_text_from_pdf(file):
    with BytesIO(file.read()) as f:
        reader = PyPDF2.PdfReader(f)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_docx(file):
    with BytesIO(file.read()) as f:
        doc = Document(f)
        return " ".join([para.text for para in doc.paragraphs if para.text])

# Semantic Match
def analyze_resume(resume_text, job_desc):
    try:
        emb_resume = model.encode(resume_text, convert_to_tensor=True)
        emb_jd = model.encode(job_desc, convert_to_tensor=True)
        score = util.pytorch_cos_sim(emb_resume, emb_jd).item()
        score_percent = round(score * 100, 2)

        recommendation = "Strong Hire" if score_percent >= 75 else "Maybe" if score_percent >= 50 else "No"
        summary = f"""
        1. **Match Score**: {score_percent}
        2. **Recommendation**: {recommendation}
        """
        return summary, score_percent, recommendation
    except Exception as e:
        return f"Error: {str(e)}", 0, "Error"

# Main UI
def main():
    st.markdown("""
    <div class="header">
        <h1>📋 AI Resume Screener</h1>
        <p>Semantic AI Matching — No API Key Required</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader("📁 Upload Resumes (PDF/DOCX)", accept_multiple_files=True)
    job_desc = st.text_area("📝 Paste Job Description", height=200, placeholder="Paste the job description here...")

    if st.button("🔍 Analyze Resumes", type="primary"):
        if not uploaded_files:
            st.error("Upload at least 1 resume")
        elif not job_desc.strip():
            st.error("Enter a job description")
        else:
            results = []
            progress_bar = st.progress(0)

            for i, file in enumerate(uploaded_files):
                try:
                    with st.expander(f"📄 {file.name}", expanded=True):
                        with st.spinner("Analyzing..."):
                            text = extract_text_from_pdf(file) if file.name.endswith('.pdf') else extract_text_from_docx(file)
                            analysis, score, rec = analyze_resume(text, job_desc)
                            st.markdown(f"""<div class="result-card">{analysis}</div>""", unsafe_allow_html=True)
                            results.append({"File Name": file.name, "Match Score (%)": score, "Recommendation": rec})
                    progress_bar.progress((i+1)/len(uploaded_files))
                    time.sleep(1)
                except Exception as e:
                    st.error(f"Failed to process {file.name}: {str(e)}")

            # Show table and download
            if results:
                df = pd.DataFrame(results)
                st.markdown("### 📊 Summary")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download Results as CSV", csv, "resume_scores.csv", "text/csv")

if __name__ == "__main__":
    main()
