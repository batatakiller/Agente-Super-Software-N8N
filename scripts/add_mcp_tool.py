import json

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

mcp_node = {
    "parameters": {
        "endpointUrl": "https://mcp.supabase.com/mcp?project_ref=qoobmxjzcjtkpezajbbv",
        "authentication": "bearerAuth",
        "options": {}
    },
    "type": "@n8n/n8n-nodes-langchain.mcpClientTool",
    "typeVersion": 1.2,
    "position": [
        -3100,
        250
    ],
    "id": "mcp-supabase-history-id",
    "name": "Historico Supabase (MCP)",
    "credentials": {
        "httpBearerAuth": {
            "id": "IxpyFYwIVzPwQbYF",
            "name": "Bearer Auth account"
        }
    }
}

def patch_mcp_tool(obj):
    if not isinstance(obj, dict):
        return
    
    if 'nodes' in obj and 'connections' in obj:
        # 1. Add MCP node if it doesn't exist
        if not any(node.get('name') == 'Historico Supabase (MCP)' for node in obj['nodes']):
            obj['nodes'].append(mcp_node)
            print("Added MCP node to a section")

        # 2. Connect MCP node to the Agent's ai_tool input
        connections = obj['connections']
        if "Historico Supabase (MCP)" not in connections:
            connections["Historico Supabase (MCP)"] = {
                "ai_tool": [[
                    {
                        "node": "Agente Super Software",
                        "type": "ai_tool",
                        "index": 0
                    }
                ]]
            }
            print("Connected MCP tool to Agente Super Software")

    # Recurse for nested blocks
    for key, value in obj.items():
        if isinstance(value, dict):
            patch_mcp_tool(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    patch_mcp_tool(item)

patch_mcp_tool(data)

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patching complete.")
