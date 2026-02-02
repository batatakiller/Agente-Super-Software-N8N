import json

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

def refactor_connections(obj):
    if not isinstance(obj, dict):
        return
    
    if 'nodes' in obj and 'connections' in obj:
        connections = obj['connections']
        
        # 1. Audio Path: Set mensagem. -> Code in JavaScript
        if "Set mensagem." in connections:
            connections["Set mensagem."]["main"] = [[
                {
                    "node": "Code in JavaScript",
                    "type": "main",
                    "index": 0
                }
            ]]
            print("Rerouted 'Set mensagem.' -> 'Code in JavaScript'")

        # 2. Unified Path: Code in JavaScript -> Guardrail Entrada
        if "Code in JavaScript" in connections:
            connections["Code in JavaScript"]["main"] = [[
                {
                    "node": "Guardrail Entrada",
                    "type": "main",
                    "index": 0
                }
            ]]
            print("Rerouted 'Code in JavaScript' -> 'Guardrail Entrada'")

        # 3. Guardrail -> Context (Ensuring it exists)
        if "Guardrail Entrada" in connections:
             connections["Guardrail Entrada"]["main"] = [[
                {
                    "node": "Carregar Contexto Híbrido",
                    "type": "main",
                    "index": 0
                }
            ]]
             print("Ensured 'Guardrail Entrada' -> 'Carregar Contexto Híbrido'")

        # 4. Context -> Agent (Ensuring it exists)
        if "Carregar Contexto Híbrido" in connections:
             connections["Carregar Contexto Híbrido"]["main"] = [[
                {
                    "node": "Agente Super Software",
                    "type": "main",
                    "index": 0
                }
            ]]
             print("Ensured 'Carregar Contexto Híbrido' -> 'Agente Super Software'")

    # Recurse
    for key, value in obj.items():
        if isinstance(value, dict):
            refactor_connections(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    refactor_connections(item)

refactor_connections(data)

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Workflow refactoring complete.")
