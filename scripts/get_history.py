import json
import urllib.request
from datetime import datetime

SUPABASE_URL = "https://qoobmxjzcjtkpezajbbv.supabase.co/rest/v1"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFvb2JteGp6Y2p0a3BlemFqYmJ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMwNDI3OTgsImV4cCI6MjA3ODYxODc5OH0.oGauqAKx1ZaMUgvYrQgvepE6XVXoKEIgbVhfWIKpgY8"

def make_request(path):
    url = f"{SUPABASE_URL}/{path}"
    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Erro: {e}")
        return []

target_suffix = "96089344"
# Mensagens desde ontem (2026-02-10)
msgs = make_request(f"whatsapp_chat?phone=ilike.%25{target_suffix}&created_at=gte.2026-02-10T18:00:00&order=created_at.asc&limit=200")

print(f"Mensagens para o final {target_suffix} desde ontem 18:00:")
for m in msgs:
    print(f"[{m['created_at']}] {m['direction']} ({m['phone']}): {m['message']}")
