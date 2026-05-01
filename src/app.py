import streamlit as st
import time
import os
import requests
import json
from dotenv import load_dotenv
from groq import Groq
from supabase import create_client, Client

# --- 1. SETUP & THEME ---
load_dotenv()
st.set_page_config(page_title="Ida.ai | Intelligent Retail", layout="centered", page_icon="🛒")

# Database & API Clients
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Custom CSS for the "Architect" Look
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    h1 { color: #00FFCC; text-align: center; font-weight: 800; letter-spacing: -1px; }
    .bill-box { 
        background-color: #111111; 
        border: 1px solid #00FFCC; 
        border-radius: 10px; padding: 20px; margin-top: 20px; 
    }
    .footer { text-align: center; font-size: 0.8em; color: #666; margin-top: 50px; }
    .stMetric { background-color: #1a1a1a; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🛒 Ida.ai")
st.markdown("<p style='text-align: center; color: #888;'>Vertical SaaS for Hyper-Localized Retail</p>", unsafe_allow_html=True)
st.write("---")

# --- 3. THE PLUMBING (BACKEND FUNCTIONS) ---
def get_transcript(audio_file):
    url = "https://api.sarvam.ai/speech-to-text"
    headers = {"api-subscription-key": os.getenv("SARVAM_API_KEY")}
    files = {"file": ("audio.mp3", audio_file, "audio/mpeg")}
    data = {"model": "saaras:v3"} 
    response = requests.post(url, headers=headers, files=files, data=data)
    return response.json().get('transcript', "")

def process_intent(transcript):
    # Fetch inventory for the LLM context
    items = supabase.table("Inventory").select("*").execute().data
    inventory_str = json.dumps(items)
    
    prompt = f"""
    You are an expert Kirana Billing Assistant.
    Transcript: "{transcript}"
    Inventory: {inventory_str}

    STRICT INSTRUCTIONS:
    1. EXTRACT BRANDS: Identify specific brands mentioned (e.g., Aavin, Gold Winner, Maggi, Parle-G, Lays, Vim, Surf Excel, Hamam, Sunsilk, Tata).
    2. ENTITY RESOLUTION: Map the transcript item to the EXACT inventory ID. 
       - "ஆவின் ஆரஞ்சு பால்" must map to the ID for "Aavin Full Cream Milk (Orange)".
       - "சன் சில்க்" must map to the ID for "Sunsilk Shampoo Sachet".
    3. NEGATION LOGIC: Handle "இல்ல" (No). If user says "3 Maggi illa 2 Maggi", the quantity is 2.
    4. MULTI-LINGUAL: Translate Tamil concepts like "சீனி" to "Sugar" or "உப்பு" to "Salt" to find the match.
    {{ "items": [{{ "id": 123, "quantity": 2, "detected_brand": "Hamam" }}] }}
    """
    
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a precise JSON extractor. Output valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    
    try:
        response_content = json.loads(chat_completion.choices[0].message.content)
        return response_content.get('items', [])
    except Exception as e:
        st.error(f"Logic Error: {e}")
        return []

# --- 4. UI FLOW ---
audio_input = st.file_uploader("Upload Transaction Audio", type=["mp3", "wav"])

if audio_input:
    st.audio(audio_input)
    
    with st.status("Initializing Neural Pipeline...", expanded=True) as status:
        st.write("🔄 Decoding Audio via Sarvam (Saaras:v3)...")
        raw_text = get_transcript(audio_input)
        time.sleep(1.5) 
        
        st.write("🧠 Parsing Intent & Semantic Matching via Groq...")
        order_items = process_intent(raw_text)
        time.sleep(1.5)
        
        status.update(label="Analysis Complete!", state="complete", expanded=False)

    # --- 5. THE OUTPUT (The "Ledger") ---
    st.markdown("<div class='bill-box'>", unsafe_allow_html=True)
    st.subheader("📜 Digital Receipt")
    
    if order_items:
        grand_total = 0
        cols = st.columns([3, 1, 1, 1])
        cols[0].write("**Item (Brand + Product)**")
        cols[1].write("**Qty**")
        cols[2].write("**Price**")
        cols[3].write("**Total**")
        
        for entry in order_items:
            item_data = supabase.table("Inventory").select("*").eq("id", entry['id']).single().execute().data
            if item_data:
                # 1. Get the brand from the AI's "detected_brand"
                # 2. If that's empty, get it from the 'Brand' column in DB
                # 3. Use Item_Name for the product type
                brand = entry.get('detected_brand', item_data.get('Brand', '')).capitalize()
                product = item_data.get('Item_Name', 'Item')
                
                # Result: "Hamam Bath Soap (100g)"
                display_name = f"{brand} {product}".strip()
                
                line_total = item_data['Selling_Price'] * entry['quantity']
                grand_total += line_total
                
                c = st.columns([3, 1, 1, 1])
                c[0].write(display_name)
                c[1].write(str(entry['quantity']))
                c[2].write(f"₹{item_data['Selling_Price']}")
                c[3].write(f"₹{line_total}")
        st.write("---")
        st.metric(label="Grand Total (Inc. GST)", value=f"₹{grand_total:,.2f}")
    else:
        st.error("Could not resolve items. Check Debug Mode below.")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- 6. THE DEBUG SECTION (For your Professors) ---
    with st.expander("🛠️ View Backend Trace (Debug Mode)"):
        st.write("**Raw Transcript:**", raw_text)
        st.write("**Parsed JSON from Groq:**", order_items)

# --- FOOTER ---
st.markdown("""
    <div class='footer'>
        Powered by SaarasV3 by Sarvam Labs| Powered by <b>Groq ⚡️</b> + <b>Llama 3.3</b>
    </div>
    """, unsafe_allow_html=True) 