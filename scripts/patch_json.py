import json

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

query_template = """SELECT 
    string_agg(formatted_message, E'\\n') AS historico_recente
FROM (
    (SELECT 
        created_at,
        'Cliente: ' || message AS formatted_message
    FROM whatsapp_chat 
    WHERE phone = '{{ $("Extrair Dados Inteligente").item.json.phone }}' 
      AND direction = 'inbound'
    ORDER BY created_at DESC 
    LIMIT 5)
    UNION ALL
    (SELECT 
        created_at,
        'Emerson (Você): ' || message AS formatted_message
    FROM whatsapp_chat 
    WHERE phone = '{{ $("Extrair Dados Inteligente").item.json.phone }}' 
      AND direction = 'outbound'
    ORDER BY created_at DESC 
    LIMIT 5)
) AS chat_unificado
ORDER BY created_at ASC;"""

new_node = {
    "parameters": {
        "operation": "executeQuery",
        "query": query_template,
        "options": {}
    },
    "id": "carregar-contexto-hibrido-id",
    "name": "Carregar Contexto Híbrido",
    "type": "n8n-nodes-base.postgres",
    "typeVersion": 2.6,
    "position": [
        -7056,
        320
    ],
    "credentials": {
        "postgres": {
            "id": "GOaED8CXwSUFbrph",
            "name": "Postgres account"
          }
    }
}

def clean_and_patch(obj):
    if not isinstance(obj, dict):
        return
    
    if 'nodes' in obj and 'connections' in obj:
        obj['nodes'] = [n for n in obj['nodes'] if n.get('name') != 'Carregar Contexto Híbrido']
        obj['nodes'].append(new_node)
        
        connections = obj['connections']
        if "Extrair Dados Inteligente" in connections:
            connections["Extrair Dados Inteligente"]["main"] = [[
                {
                    "node": "Carregar Contexto Híbrido",
                    "type": "main",
                    "index": 0
                }
            ]]
        connections["Carregar Contexto Híbrido"] = {
            "main": [[
                {
                    "node": "Apenas Dados Válidos",
                    "type": "main",
                    "index": 0
                }
            ]]
        }

    for key, value in obj.items():
        if isinstance(value, dict):
            clean_and_patch(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    clean_and_patch(item)

clean_and_patch(data)

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done cleaning and patching with UTF-8.")
