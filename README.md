# 📝 Handwritten Notes AI

A fully local, privacy-first Retrieval-Augmented Generation (RAG) system that reads handwritten PDF notes, indexes them, and allows you to chat with your documents using state-of-the-art offline AI.

![Hero Banner](https://img.shields.io/badge/100%25_Offline-Privacy_First-059669?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-4f46e5?style=for-the-badge&logo=ollama)
![Streamlit](https://img.shields.io/badge/Streamlit-Premium_UI-FF4B4B?style=for-the-badge&logo=streamlit)

## ✨ Features

- **100% Offline & Private**: Zero cloud APIs. No data ever leaves your machine. Powered by local embeddings and Ollama.
- **Handwriting Recognition**: Utilizes `EasyOCR` and `pdf2image` to accurately digitize scanned handwritten notes.
- **Smart Document Caching**: Near instant re-processing if a document has been uploaded before.
- **Premium UI/UX**: Features a highly-polished, Notion-style minimalist interface with full native **Light & Dark modes**, CSS variable theming, and real-time streaming responses.
- **Auto-Summarization & Quick Actions**: Instantly generates an executive summary on upload and provides interactive Quick Action buttons (Summarize, Key Takeaways, Quiz Me).
- **Intelligent RAG Pipeline**: High-accuracy context retrieval using `ChromaDB` and `SentenceTransformers`, providing exact source page citations for every claim.

## 🛠️ Technology Stack

- **Frontend Integration**: Streamlit
- **Vision & OCR**: EasyOCR (PyTorch), Poppler (`pdf2image`)
- **Vector Database**: ChromaDB (Local SQLite backend)
- **Embeddings Pipeline**: SentenceTransformers (`all-MiniLM-L6-v2`)
- **LLM Engine**: Ollama (Using `gemma:4b` by default)

## 🚀 Getting Started

### Prerequisites
Before running the application, ensure you have the following installed:
1. **Python 3.10+**
2. **[Ollama](https://ollama.ai/)**: Installed and running in the background.
3. **Poppler for Windows**: Extract the Poppler binaries to a folder (e.g., `C:\poppler\bin`), and ensure that path is added to your System `PATH` environment variable.

### Installation

1. **Clone the repository:**
```bash
git clone <your-repository-url>
cd handwritten-notes-assistant
```

2. **Set up a virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\activate   # On Windows PowerShell
# source venv/bin/activate # On Unix/macOS
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Pull Local LLM Model:**
Make sure Ollama is running, then download the model:
```bash
ollama pull gemma:4b
```
*(Note: You can easily swap this out for `llama3`, `mistral`, etc., by updating the model name in `src/config.py`)*

### Running the App
Start the Streamlit server:
```bash
streamlit run app.py
```
*The app will automatically open in your browser at `http://localhost:8501`*

## 📁 Project Architecture

```plaintext
handwritten-notes-assistant/
├── app.py                  # Main Streamlit application and UI definitions
├── src/
│   ├── config.py           # Core configuration, paths, and model selection
│   ├── llm_engine.py       # Ollama chat generation logic
│   ├── ocr_pipeline.py     # PDF to Image conversion + EasyOCR engine
│   └── vector_db.py        # ChromaDB ingestion, chunking, and search
├── data/
│   ├── db/                 # Vector database local storage
│   ├── uploads/            # Temporary PDF storage
│   └── cache_ocr/          # JSON caches for instant secondary loads
└── requirements.txt        # Project dependencies
```

## 🧠 How it Works underlyingly
1. **Ingestion**: You drag and drop a handwritten PDF. The UI saves it to the `data/uploads` directory.
2. **Vision & OCR**: `pdf2image` converts the PDF into optimized images. `EasyOCR` scans the handwriting on each image and extracts the raw text. Wait times are minimized through active pixel downscaling.
3. **Embed & Index**: The raw text is cleaned, split into overlapping chunks, mathematically mapped using `SentenceTransformers`, and saved to a local `ChromaDB` instance.
4. **Chat & Retrieve**: Whenever a question is asked, ChromaDB performs a similarity search against the vectors and pulls the top 5 most relevant chunks.
5. **Generation**: The prompt, alongside the retrieved context from the handwritten notes, is sent to the local `Ollama` model which streams back a contextually accurate response.



