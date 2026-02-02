import json
import os

def extract_recursive(obj, node_id):
    if isinstance(obj, dict):
        if obj.get('id') == node_id:
            if 'parameters' in obj and 'options' in obj['parameters'] and 'systemMessage' in obj['parameters']['options']:
                prompt = obj['parameters']['options']['systemMessage']
                # Remove starting '=' if present (n8n expression identifier)
                if prompt.startswith('='):
                    prompt = prompt[1:]
                return prompt
        for k, v in obj.items():
            result = extract_recursive(v, node_id)
            if result:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = extract_recursive(item, node_id)
            if result:
                return result
    return None

def main():
    json_path = 'Agente SuperSoftware.json'
    prompt_path = 'system_prompt.md'
    node_id = 'f0de20ef-63cf-4ce1-8425-2b58111c01c3'

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    prompt = extract_recursive(data, node_id)
    
    if prompt:
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"✅ Successfully extracted prompt to {prompt_path}")
    else:
        print(f"⚠️ No nodes found with ID {node_id} or missing systemMessage")

if __name__ == "__main__":
    main()
