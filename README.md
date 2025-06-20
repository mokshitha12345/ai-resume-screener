# 📋 AI Resume Screener

An AI-powered resume screening tool built with Streamlit and Sentence Transformers.

## 🔍 What It Does
- Upload multiple resumes (PDF/DOCX)
- Paste a job description
- Uses a fine-tuned Sentence Transformer model to calculate semantic similarity
- Displays match scores and recommendations (Strong Hire / Maybe / No)
- Exports results to CSV

## 🚀 Tech Stack
- **Frontend**: Streamlit
- **Backend**: Sentence Transformers (all-MiniLM-L6-v2)
- **Parsing**: PyPDF2 for PDFs, python-docx for DOCX
- **Similarity**: Cosine similarity from `sentence-transformers.util`

## 🛠 Setup

1. Clone the repo:
    ```bash
    git clone https://github.com/your-username/ai-resume-screener.git
    cd ai-resume-screener
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the app:
    ```bash
    streamlit run app.py
    ```

## 🌐 Streamlit Cloud Deployment

Make sure your GitHub repo contains:
- `app.py`
- `requirements.txt`
- (Optional) `README.md`
- Any model folders like `fine_tuned_resume_model/` if needed

Then deploy from [Streamlit Cloud](https://streamlit.io/cloud).

---

## 👩‍💻 Author
**M. Mokshitha**  
📧 m.mokshitha06@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/mokshitha-minamanuri)  
🔗 [GitHub](https://github.com/mokshitha12345)
