
import json
import os

def update_recursive(obj, node_id, new_prompt):
    count = 0
    if isinstance(obj, dict):
        if obj.get('id') == node_id:
            if 'parameters' in obj and 'options' in obj['parameters'] and 'systemMessage' in obj['parameters']['options']:
                # Prepend '=' for n8n expression
                obj['parameters']['options']['systemMessage'] = "=" + new_prompt
                count += 1
        for k, v in obj.items():
            count += update_recursive(v, node_id, new_prompt)
    elif isinstance(obj, list):
        for item in obj:
            count += update_recursive(item, node_id, new_prompt)
    return count

def main():
    prompt_path = 'system_prompt.md'
    json_path = 'Agente SuperSoftware.json'
    node_id = 'f0de20ef-63cf-4ce1-8425-2b58111c01c3'

    if not os.path.exists(prompt_path):
        print(f"Error: {prompt_path} not found.")
        return

    with open(prompt_path, 'r', encoding='utf-8') as f:
        new_prompt = f.read().strip()

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updates = update_recursive(data, node_id, new_prompt)
    
    if updates > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Successfully updated {updates} node(s) in {json_path}")
    else:
        print(f"⚠️ No nodes found with ID {node_id}")

if __name__ == "__main__":
    main()
