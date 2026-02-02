import json

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define the new Filter node
security_filter_node = {
    "parameters": {
        "conditions": {
            "string": [
                {
                    "value1": "={{ $json.text }}",
                    "value2": "VALIDA"
                }
            ]
        }
    },
    "id": "filtro-seguranca-id",
    "name": "Filtro de Segurança",
    "type": "n8n-nodes-base.if",
    "typeVersion": 1,
    "position": [
        -3180,
        -16
    ]
}

def apply_security_filter(obj):
    if not isinstance(obj, dict):
        return
    
    if 'nodes' in obj and 'connections' in obj:
        # Add the node if missing
        if not any(n.get('name') == 'Filtro de Segurança' for n in obj['nodes']):
            obj['nodes'].append(security_filter_node)
            print("Added 'Filtro de Segurança' node.")

        conns = obj['connections']
        
        # Guardrail -> Filtro de Segurança
        if "Guardrail Entrada" in conns:
            conns["Guardrail Entrada"]["main"] = [[
                {
                    "node": "Filtro de Segurança",
                    "type": "main",
                    "index": 0
                }
            ]]
            print("Connected 'Guardrail Entrada' -> 'Filtro de Segurança'")

        # Filtro de Segurança (True) -> Carregar Contexto Híbrido
        conns["Filtro de Segurança"] = {
            "main": [
                [
                    {
                        "node": "Carregar Contexto Híbrido",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
        print("Connected 'Filtro de Segurança' (True) -> 'Carregar Contexto Híbrido'")

    # Recurse
    for key, value in obj.items():
        if isinstance(value, dict):
            apply_security_filter(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    apply_security_filter(item)

apply_security_filter(data)

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Security filter implementation complete.")
