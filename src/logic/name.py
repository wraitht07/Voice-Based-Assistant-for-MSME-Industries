import os
from dotenv import load_dotenv
from supabase import create_client
from groq import Groq
import bill_calc
import json
import requests
load_dotenv()
# --- 1. SARVAM STT FUNCTION ---
def get_sarvam_transcript(file_path):
    api_key = os.getenv("SARVAM_API_KEY")
    url = "https://api.sarvam.ai/speech-to-text"
    
    files = {
        'file': (os.path.basename(file_path), open(file_path, 'rb'), 'audio/mpeg')
    }
    payload = {
        'model': 'saaras:v3',
        'language_code': 'ta-IN' 
    }
    headers = {'api-subscription-key': api_key}
    
    print(f"👂 Processing Voice: {file_path}...")
    response = requests.post(url, headers=headers, data=payload, files=files)
    
    if response.status_code == 200:
        return response.json().get('transcript')
    else:
        print(f"❌ Sarvam Error: {response.text}")
        return None
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"))
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_ANON_KEY")
clientv1=create_client("https://qsmkmodsksqnsdlpwqcl.supabase.co","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFzbWttb2Rza3NxbnNkbHB3cWNsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYwODk0MzAsImV4cCI6MjA5MTY2NTQzMH0.j1UL8yqQOMGuIhPT5nU3YzMcOnSh3HeSaNH_WXb2SgM"
)
response=clientv1.table("Inventory").select("id","Item_Name","Keywords","Selling_Price", "GST_Percent").execute()
inventory_list=response.data

audio_file = "Myvoice.mp3" 
transcript = get_sarvam_transcript(audio_file)

if transcript:
    print(f"📝 AI Heard: {transcript}")
    completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system", 
            "content": f"""
            You are a Retail Transaction Parser. 
            Inventory: {inventory_list}
            
            STRICT RULES:
            1. Language: The input may be in Tamil Script (e.g., அரை, ஒன்று), Tanglish (e.g., Arai, Onnu), or English. 
            2. Quantities:
            - 'அரை' / 'Arai' / 'Half' = 0.5
            - 'கால்' / 'Kaal' / 'Quarter' = 0.25
            - 'ஒன்று' / 'Onnu' / 'Oru' / '1' = 1
            - 'இரண்டு' / 'Rendu' / '2' = 2
            3. Matching: Use the 'Keywords' and 'Item_Name' from the Inventory to find the correct ID. 
            Example: "பாக்கெட் லேஸ்" or "Blue Lays" should both map to ID 10.
            4. Task: Extract EVERY item mentioned in the transcript.
            "5. Corrections: If the user corrects themselves (e.g., 'no, make it 2' or 'illa rendu'), ignore the first value and only output the final intended quantity."
        
            OUTPUT ONLY VALID JSON:
            {{"items": [{{"id": 10, "qty": 1}}, {{"id": 5, "qty": 0.5}}]}}"""
        },
        {
            "role": "user",
            "content": str(transcript) # "Arai kilo Pacha Arisi,blue packet lays,sunsilk shampoo onnu,seeraga samba arisi"
        }
    ],
    response_format={"type": "json_object"}
)

data = json.loads(completion.choices[0].message.content)
order_items = data.get("items", []) # This MUST be a list

print("--- SHOPPING BILL ---")
grand_total = 0

for item in order_items: # This loop ensures we don't just print the last one
    # Match ID from your inventory_list
    match = next((i for i in inventory_list if i['id'] == item['id']), None)
    
    if match:
        res = bill_calc.calculate_item(
            match['Item_Name'], 
            item['qty'], 
            match['Selling_Price'], 
            match['GST_Percent']
        )
        print(res['text'])
        grand_total += res['Total']

print(f"-------\nGRAND TOTAL: ₹{round(grand_total, 2)}")


