import json

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

def fix_agent_prompt(obj):
    if not isinstance(obj, dict):
        return
    
    if 'nodes' in obj:
        for node in obj['nodes']:
            if node.get('name') == 'Agente Super Software':
                # Update the main text/prompt parameter
                if 'parameters' in node:
                    # Point to Code in JavaScript where the prompt is normalized
                    node['parameters']['text'] = "={{ $('Code in JavaScript').first().json.input }}"
                    print("Updated Agent prompt to reference Guardrail Entrada.")

    # Recurse
    for key, value in obj.items():
        if isinstance(value, dict):
            fix_agent_prompt(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    fix_agent_prompt(item)

fix_agent_prompt(data)

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Agent prompt fix complete.")
