🛒 Ida.ai: Hyper-Localized AI Retail Engine
Vertical SaaS for the Indian Kirana Ecosystem
Ida.ai is an intelligent billing and inventory management prototype designed to bridge the digital gap for traditional retail shopkeepers. By leveraging specialized Speech-to-Text (STT) and Large Language Models (LLMs), the system converts spontaneous, multi-lingual, and noisy audio orders into structured, ACID-compliant ledger transactions.

🚀 The Core Problem
Most retail POS (Point of Sale) systems are designed for English-speaking, desk-bound environments. Traditional Indian Kirana stores face:

High Friction: Shopkeepers cannot type while handling products.
Acoustic Challenges: High background noise and reverberation (the "Well" effect).
The "Tanglish" Dialect: Spontaneous code-switching between Tamil and English.
Intent Correction: Customers frequently stutter or change their minds mid-order (e.g., "3 Maggi... no, make it 2").
🛠️ Technical Architecture
1. Acoustic Intelligence (The Ears)
Engine: Sarvam AI - Saaras:v3
Logic: We utilized Saaras:v3 specifically for its robustness against spontaneous speech and Indian accents. It handles the "Tanglish" input and outputs a raw transcript that preserves the nuances of the shopkeeper's dialogue.
2. Semantic Mapping & Logic (The Brain)
Engine: Groq (Llama 3.3 70B)
Function: Performs Named Entity Recognition (NER) and Intent Parsing.
Fuzzy Logic: The model maps colloquial Tamil terms (e.g., சீனி/Seeni) to formal Inventory SKUs (e.g., Sugar). It also processes logical negations like "Illa" (No) to update quantities dynamically before they hit the database.
3. Data Integrity (The Ledger)
Engine: Supabase (PostgreSQL)
Compliance: Built on a relational foundation to ensure ACID compliance. Every voice-generated bill is cross-referenced against a master Inventory table to ensure pricing accuracy and SKU integrity.
📦 Key Features
Zero-Touch Billing: Entire orders generated via voice.
Brand-First Extraction: Prioritizes manufacturer names (Sunsilk, Aavin, Tata) over generic categories.
Hyper-Localized: Specifically tuned for the Tamil retail context.
Real-time Inference: Powered by Groq for sub-second processing speed.
📂 Project Structure
├── app.py              # Streamlit UI & Orchestration Logic
├── .env                # Secure Environment Variables (API Keys)
├── requirements.txt    # System Dependencies
└── README.md           # Documentation
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
streamlit run app.py
🛤️ Future Roadmap
To move Ida.ai from a prototype to a production-grade enterprise solution, the following architectural upgrades are planned:

1. Vector Search for Large-Scale Inventories
As inventory grows beyond 10,000+ SKUs, the current "Full-Context" injection will hit token limits.

The Upgrade: Implement RAG (Retrieval-Augmented Generation) using the pgvector extension in Supabase.
The Impact: This allows the system to perform a "Semantic Search" on product descriptions, retrieving only the top 10 relevant items for the LLM to choose from, significantly reducing latency and costs.
2. Multi-Tenant Database Architecture
To support thousands of different Kirana shops on a single platform.

The Upgrade: Implement a Schema-based Multi-tenancy or shop_id partitioning.
The Impact: Ensures strict data isolation so Shop A cannot see Shop B's inventory or sales data, while allowing a single backend to scale horizontally.
3. Edge Computing for Low Latency
In areas with poor internet connectivity (common in rural retail).

The Upgrade: Deploy the STT engine (Sarvam) and a smaller LLM (like Llama 3-8B) on Edge Devices or local servers.
The Impact: Reduces "Time-to-First-Token" and allows the shop to continue billing even when the external internet is unstable.
4. Predictive Inventory Analytics
The Upgrade: Integrate a forecasting module using historical sales data stored in PostgreSQL.
The Impact: The system can automatically voice-alert the shopkeeper: "You are low on Aavin Orange Milk; should I add it to the distributor order?"

