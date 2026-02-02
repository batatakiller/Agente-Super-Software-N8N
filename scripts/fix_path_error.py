import json

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# The new query should reference 'Info' instead of 'Extrair Dados Inteligente'
# Because 'Info' is in the main path that reaches the agent.
new_query = """SELECT 
    string_agg(formatted_message, E'\\n') AS historico_recente
FROM (
    (SELECT 
        created_at,
        'Cliente: ' || message AS formatted_message
    FROM whatsapp_chat 
    WHERE phone = '{{ $("Info").item.json.telefone }}' 
      AND direction = 'inbound'
    ORDER BY created_at DESC 
    LIMIT 5)
    UNION ALL
    (SELECT 
        created_at,
        'Emerson (Você): ' || message AS formatted_message
    FROM whatsapp_chat 
    WHERE phone = '{{ $("Info").item.json.telefone }}' 
      AND direction = 'outbound'
    ORDER BY created_at DESC 
    LIMIT 5)
) AS chat_unificado
ORDER BY created_at ASC;"""

def fix_path_error(obj):
    if not isinstance(obj, dict):
        return
    
    if 'nodes' in obj and 'connections' in obj:
        # 1. Update the Carregar Contexto Híbrido node
        for node in obj['nodes']:
            if node.get('name') == 'Carregar Contexto Híbrido':
                node['parameters']['query'] = new_query
                # Move it near the agent
                node['position'] = [-3150, -150]
                print("Updated Context node query and position.")

        # 2. Update connections
        connections = obj['connections']
        
        # Remove old connection Extrair -> Carregar
        if "Extrair Dados Inteligente" in connections:
            connections["Extrair Dados Inteligente"]["main"] = [[
                {
                    "node": "Apenas Dados Válidos",
                    "type": "main",
                    "index": 0
                }
            ]]
            print("Fixed Extrair -> Apenas branch (skipped context).")

        # Rewire Guardrail Entrada -> Context -> Agent
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
                    "node": "Agente Super Software",
                    "type": "main",
                    "index": 0
                }
            ]]
        }
        print("Linked Context -> Agente Super Software.")

    # Recurse
    for key, value in obj.items():
        if isinstance(value, dict):
            fix_path_error(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    fix_path_error(item)

fix_path_error(data)

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Path fix complete.")
