# 🛒 Ida.ai: Hyper-Localized AI Retail Engine
### *Vertical SaaS for the Indian Kirana Ecosystem*

**Ida.ai** is an intelligent billing and inventory management prototype designed to bridge the digital gap for traditional retail shopkeepers. By leveraging specialized **Speech-to-Text (STT)** and **Large Language Models (LLMs)**, the system converts spontaneous, multi-lingual, and noisy audio orders into structured, ACID-compliant ledger transactions.

---

## 🚀 The Core Problem
Traditional Indian Kirana stores face unique digital hurdles:
* **High Friction:** Shopkeepers cannot type while handling products.
* **Acoustic Challenges:** High background noise and reverberation.
* **The "Tanglish" Dialect:** Spontaneous code-switching between Tamil and English.
* **Intent Correction:** Processing logical negations (e.g., *"3 Maggi... no, make it 2"*).

---

## 🛠️ Technical Architecture



1. **Acoustic Intelligence:** `Sarvam AI - Saaras:v3` for robust "Tanglish" transcription.
2. **Semantic Mapping:** `Groq (Llama 3.3 70B)` for NER and Intent Parsing.
3. **Data Integrity:** `Supabase (PostgreSQL)` for ACID-compliant inventory management.

---

## 📂 Project Structure
```text
Ida-AI/
├── .github/              # Issue templates and CI workflows
├── src/
│   ├── logic/            # Intent parsing and mapping algorithms
│   ├── utils/            # Audio processing and API helpers
│   └── app.py            # Streamlit UI & Orchestration Logic
├── .gitignore            # Standard Python/Streamlit exclusions
├── requirements.txt      # System Dependencies
└── README.md             # Project Documentation
```
🚦Getting Started

### 1. Install Dependencies
Run the following command to set up the necessary libraries:
```bash
pip install streamlit groq requests python-dotenv supabase
```

### 2. Configure Environment Variables
Create a file named `.env` in the root directory and add your credentials:
```text
GROQ_API_KEY=your_key_here
SARVAM_API_KEY=your_key_here
SUPABASE_URL=your_url_here
SUPABASE_ANON_KEY=your_key_here
```

### 3. Launch the Application
Start the Streamlit interface with:
```bash
streamlit run src/app.py
```

🛤️ Future Roadmap
```
🔍 Vector Search (pgvector): Implement RAG (Retrieval-Augmented Generation) to handle 10,000+ SKUs efficiently without hitting LLM token limits.

🏗️ Multi-Tenant Architecture: Use schema-based isolation to allow thousands of different Kirana shops to use the platform securely.

🌐 Edge Computing: Deploy local LLMs (like Llama 3-8B) for offline billing capability in areas with unstable internet connectivity.

📈 Predictive Analytics: Integrate a forecasting module to alert shopkeepers when essential stock is running low based on historical trends.
```


