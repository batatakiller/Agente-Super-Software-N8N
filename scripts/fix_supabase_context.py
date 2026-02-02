import json

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Define the new Supabase node (Carregar Contexto Híbrido)
new_supabase_node = {
    "parameters": {
        "operation": "getAll",
        "tableId": "whatsapp_chat",
        "returnAll": False,
        "limit": 20,
        "filters": {
            "conditions": [
                {
                    "keyName": "phone",
                    "keyValue": "={{ $('Info').item.json.telefone }}"
                }
            ]
        },
        "options": {
            "sort": [
                {
                    "column": "created_at",
                    "direction": "desc"
                }
            ]
        }
    },
    "id": "carregar-contexto-hibrido-id",
    "name": "Carregar Contexto Híbrido",
    "type": "n8n-nodes-base.supabase",
    "typeVersion": 1,
    "position": [
        -3150,
        -150
    ],
    "credentials": {
        "supabaseApi": {
            "id": "uRNDmQF562RElzxd",
            "name": "Supabase account"
        }
    }
}

# 2. Define the new Code node (Formatar Historico)
new_code_node = {
    "parameters": {
        "jsCode": """
const items = $input.all();
if (items.length === 0) {
    return [{ json: { historico_recente: "Nenhum histórico encontrado." } }];
}

const rawMessages = items.map(i => i.json);

// Separar e pegar os últimos 5 de cada (já vêm ordenados por desc no Supabase)
const inbound = rawMessages.filter(m => m.direction === 'inbound').slice(0, 5);
const outbound = rawMessages.filter(m => m.direction === 'outbound').slice(0, 5);

// Unificar, formatar e ordenar cronologicamente (ASC)
const finalHistory = [...inbound, ...outbound]
    .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
    .map(m => {
        const prefix = m.direction === 'inbound' ? 'Cliente: ' : 'Emerson (Você): ';
        return `${prefix}${m.message}`;
    })
    .join('\\n');

return [{ json: { historico_recente: finalHistory || "Sem histórico relevante." } }];
"""
    },
    "id": "formatar-historico-id",
    "name": "Formatar Historico",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [
        -2900,
        -150
    ]
}

def fix_credentials_and_type(obj):
    if not isinstance(obj, dict):
        return
    
    if 'nodes' in obj and 'connections' in obj:
        # Replace the node
        obj['nodes'] = [n for n in obj['nodes'] if n.get('name') != 'Carregar Contexto Híbrido']
        obj['nodes'].append(new_supabase_node)
        obj['nodes'].append(new_code_node)
        print("Replaced Context node and added Formatter node.")

        connections = obj['connections']
        
        # Rewire: Guardrail -> Context -> Formatter -> Agent
        if "Guardrail Entrada" in connections:
            connections["Guardrail Entrada"]["main"] = [[
                {
                    "node": "Carregar Contexto Híbrido",
                    "type": "main",
                    "index": 0
                }
            ]]
            print("Linked Guardrail Entrada -> Context.")

        connections["Carregar Contexto Híbrido"] = {
            "main": [[
                {
                    "node": "Formatar Historico",
                    "type": "main",
                    "index": 0
                }
            ]]
        }
        
        connections["Formatar Historico"] = {
            "main": [[
                {
                    "node": "Agente Super Software",
                    "type": "main",
                    "index": 0
                }
            ]]
        }
        print("Linked Context -> Formatter -> Agente Super Software.")

    # Recurse
    for key, value in obj.items():
        if isinstance(value, dict):
            fix_credentials_and_type(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    fix_credentials_and_type(item)

fix_credentials_and_type(data)

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Supabase migration complete.")
