import json

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_and_replace(obj):
    if not isinstance(obj, dict):
        return
    
    if 'nodes' in obj and 'connections' in obj:
        # 1. Remove Historico Supabase (MCP)
        obj['nodes'] = [n for n in obj['nodes'] if n.get('name') != 'Historico Supabase (MCP)']
        
        connections = obj['connections']
        if 'Historico Supabase (MCP)' in connections:
            del connections['Historico Supabase (MCP)']
            
        # 2. Add connection for "Get a row in Supabase" if not exists
        if 'Get a row in Supabase' in connections:
            # Ensure it's connected as ai_tool to the agent
            if 'ai_tool' not in connections['Get a row in Supabase']:
                connections['Get a row in Supabase']['ai_tool'] = [[
                    {
                        "node": "Agente Super Software",
                        "type": "ai_tool",
                        "index": 0
                    }
                ]]
            print("Ensured 'Get a row in Supabase' is connected as a tool.")
        else:
            # Maybe the node exists but doesn't have an entry in connections yet?
            # Let's add it just in case.
            connections['Get a row in Supabase'] = {
                "ai_tool": [[
                    {
                        "node": "Agente Super Software",
                        "type": "ai_tool",
                        "index": 0
                    }
                ]]
            }
            print("Created connection for 'Get a row in Supabase'.")

    # Recurse
    for key, value in obj.items():
        if isinstance(value, dict):
            clean_and_replace(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    clean_and_replace(item)

clean_and_replace(data)

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done swapping tools.")
