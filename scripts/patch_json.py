import json
import os

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r') as f:
    data = json.load(f)

new_node = {
    "parameters": {
        "operation": "executeQuery",
        "query": "SELECT \n    string_agg(formatted_message, E'\\n') AS historico_recente\nFROM (\n    (SELECT \n        created_at,\n        'Cliente: ' || message AS formatted_message\n    FROM whatsapp_chat \n    WHERE phone = '{{ $(\\'Extrair Dados Inteligente\\').item.json.phone }}' \n      AND direction = 'inbound'\n    ORDER BY created_at DESC \n    LIMIT 5)\n    UNION ALL\n    (SELECT \n        created_at,\n        'Emerson (Você): ' || message AS formatted_message\n    FROM whatsapp_chat \n    WHERE phone = '{{ $(\\'Extrair Dados Inteligente\\').item.json.phone }}' \n      AND direction = 'outbound'\n    ORDER BY created_at DESC \n    LIMIT 5)\n) AS chat_unificado\nORDER BY created_at ASC;",
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

def patch_nodes_and_connections(obj):
    if not isinstance(obj, dict):
        return
    
    if 'nodes' in obj and 'connections' in obj:
        # 1. Add node if not exists
        if not any(node.get('name') == 'Carregar Contexto Híbrido' for node in obj['nodes']):
            obj['nodes'].append(new_node)
            print(f"Added node to a section")
        else:
            # Update existing node to ensure correct query (no extra backslashes)
            for node in obj['nodes']:
                if node.get('name') == 'Carregar Contexto Híbrido':
                    node['parameters']['query'] = new_node['parameters']['query']
            print(f"Updated node query in a section")

        # 2. Update connections
        connections = obj['connections']
        
        # Link Extrair -> Carregar
        if "Extrair Dados Inteligente" in connections:
            connections["Extrair Dados Inteligente"]["main"] = [[
                {
                    "node": "Carregar Contexto Híbrido",
                    "type": "main",
                    "index": 0
                }
            ]]
        
        # Link Carregar -> Apenas
        connections["Carregar Contexto Híbrido"] = {
            "main": [[
                {
                    "node": "Apenas Dados Válidos",
                    "type": "main",
                    "index": 0
                }
            ]]
        }
        print(f"Updated connections in a section")

    # Recurse for nested blocks like activeVersion
    for key, value in obj.items():
        if isinstance(value, dict):
            patch_nodes_and_connections(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    patch_nodes_and_connections(item)

patch_nodes_and_connections(data)

with open(filepath, 'w') as f:
    json.dump(data, f, indent=2)

print("Done patching.")
