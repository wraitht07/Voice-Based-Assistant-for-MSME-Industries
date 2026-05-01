🛒 Ida.ai: Hyper-Localized AI Retail Engine
Vertical SaaS for the Indian Kirana Ecosystem
Ida.ai is an intelligent billing and inventory management prototype designed to bridge the digital gap for traditional retail shopkeepers. By leveraging specialized Speech-to-Text (STT) and Large Language Models (LLMs), the system converts spontaneous, multi-lingual, and noisy audio orders into structured, ACID-compliant ledger transactions.

🚀 The Core Problem
Traditional Indian Kirana stores face unique digital hurdles that standard POS systems ignore:

High Friction: Shopkeepers cannot type while physically handling and bagging products.

Acoustic Challenges: High background noise and reverberation (the "Well" effect) in small shops.

The "Tanglish" Dialect: Spontaneous code-switching between Tamil and English.

Intent Correction: Customers frequently stutter or change their minds mid-order (e.g., "3 Maggi... no, make it 2").

🛠️ Technical Architecture
1. Acoustic Intelligence (The Ears)
Engine: Sarvam AI - Saaras:v3

Logic: Chosen for its robustness against Indian accents and spontaneous speech. It preserves the nuances of "Tanglish" dialogue, outputting a raw transcript that captures the shopkeeper's natural flow.

2. Semantic Mapping & Logic (The Brain)
Engine: Groq (Llama 3.3 70B)

Function: Performs Named Entity Recognition (NER) and Intent Parsing.

Fuzzy Logic: Maps colloquial Tamil terms (e.g., சீனி/Seeni) to formal Inventory SKUs (e.g., Sugar). It processes logical negations like "Illa" (No) to update quantities dynamically before database insertion.

3. Data Integrity (The Ledger)
Engine: Supabase (PostgreSQL)

Compliance: Built on a relational foundation to ensure ACID compliance. Every voice-generated bill is cross-referenced against a master Inventory table to ensure pricing accuracy and SKU integrity.

📦 Key Features
🎙️ Zero-Touch Billing: Entire orders generated via hands-free voice commands.

🏷️ Brand-First Extraction: Prioritizes manufacturer names (Sunsilk, Aavin, Tata) over generic categories.

📍 Hyper-Localized: Specifically tuned for the Tamil retail context and spontaneous code-switching.

⚡ Real-time Inference: Powered by Groq for sub-second processing speed.

📂 Project Structure
Ida-AI/
├── .github/              # Issue templates and CI workflows
├── src/
│   ├── logic/            # Intent parsing and mapping algorithms
│   ├── utils/            # Audio processing and API helpers
│   └── app.py            # Streamlit UI & Orchestration Logic
├── .gitignore            # Standard Python/Streamlit exclusions
├── requirements.txt      # System Dependencies
└── README.md             # Project Documentation

🚦 Getting Started
1. Install Dependencies
   pip install streamlit groq requests python-dotenv supabase
2. Configure Environment Variables
   Create a .env file in the root directory:
   GROQ_API_KEY=your_key_here
  SARVAM_API_KEY=your_key_here
  SUPABASE_URL=your_url_here
  SUPABASE_ANON_KEY=your_key_here
3. Launch the Application
   streamlit run src/app.py
🛤️ Future Roadmap
To move Ida.ai from a prototype to a production-grade enterprise solution:
Vector Search (pgvector): Implement RAG to handle 10,000+ SKUs without hitting LLM token limits.

Multi-Tenant Architecture: Implement shop_id partitioning to support thousands of stores on a single platform with strict data isolation.

Edge Computing: Deploy smaller models (Llama 3-8B) locally to allow offline billing in areas with unstable internet.

Predictive Analytics: Use historical sales data to provide voice-alerts for low stock (e.g., "You are low on Aavin Milk; shall I reorder?").
