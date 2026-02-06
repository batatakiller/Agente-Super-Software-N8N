#!/usr/bin/env python3
import json
import sys
import urllib.request
from datetime import datetime

# Supabase Credentials
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
        print(f"Erro ao acessar Supabase: {e}")
        return []

def format_date(date_str):
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M:%S')
    except:
        return date_str

def search_conversation(phone):
    # Limpar telefone (apenas números)
    clean_phone = "".join(filter(str.isdigit, phone))
    
    # Formatos de busca
    variants = [clean_phone]
    if not clean_phone.startswith("55"):
        variants.append("55" + clean_phone)
    else:
        variants.append(clean_phone[2:])
    
    print(f"\n🔍 Buscando por variantes: {', '.join(variants)}")

    # 1. Buscar no amazon_orders_raw para identificar o cliente
    customer_name = "Não encontrado"
    order_id = "N/A"
    for v in variants:
        # Busca flexível por parte do número
        orders = make_request(f"amazon_orders_raw?buyer-phone-number=ilike.%25{v[-8:]}%25&limit=1")
        if orders:
            customer_name = orders[0].get("buyer-name", "N/A")
            order_id = orders[0].get("order-id", "N/A")
            break

    print(f"👤 Cliente: {customer_name.upper()}")
    print(f"📦 Pedido: {order_id}")
    print("-" * 50)

    # 2. Buscar no whatsapp_chat (Busca flexível pelos últimos 8 dígitos)
    last_8 = clean_phone[-8:]
    print(f"📡 Buscando mensagens vinculadas ao final ...{last_8}")
    
    unique_msgs = make_request(f"whatsapp_chat?phone=ilike.%25{last_8}&order=created_at.desc&limit=100")
    
    # Ordenar cronologicamente
    unique_msgs.sort(key=lambda x: x['created_at'])

    if not unique_msgs:
        print("❌ Nenhuma mensagem encontrada.")
        return

    for m in unique_msgs:
        dir_label = "Emerson (Você)" if m['direction'] in ['outbound', 'sent'] else "Cliente"
        msg_text = m['message'].replace("\n", " ")
        if False:
            msg_text = msg_text[:77] + "..."
        
        print(f"[{format_date(m['created_at'])}] {dir_label}: {msg_text}")
    print("-" * 50)
    print(f"✅ Total: {len(unique_msgs)} mensagens.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 search_chat.py <telefone>")
        sys.exit(1)
    
    search_conversation(sys.argv[1])
