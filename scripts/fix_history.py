import json

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

def fix_history_nodes(obj):
    if not isinstance(obj, dict):
        return
    
    if 'nodes' in obj:
        # 1. Update Carregar Contexto Híbrido
        for node in obj['nodes']:
            if node.get('name') == 'Carregar Contexto Híbrido':
                if 'parameters' in node:
                    node['parameters']['limit'] = 50
                    print("Increased limit to 50 in Carregar Contexto Híbrido.")
        
        # 2. Update Formatar Historico and remove duplicates
        formatar_nodes = [n for n in obj['nodes'] if n.get('name') == 'Formatar Historico']
        if formatar_nodes:
            # Keep the first one, remove others
            primeiro = formatar_nodes[0]
            # Remove all and re-add only the first
            nodes_sem_formatar = [n for n in obj['nodes'] if n.get('name') != 'Formatar Historico']
            obj['nodes'] = nodes_sem_formatar + [primeiro]
            
            # Update jsCode
            new_code = """
const items = $input.all();
if (items.length === 0) {
    return [{ json: { historico_recente: "Nenhum histórico encontrado." } }];
}

// Supabase retorna DESC (mais recentes primeiro)
const rawMessages = items.map(i => i.json);

// Pegar as últimas 20 mensagens, reverter para ordem cronológica (ASC)
const finalHistory = rawMessages
    .slice(0, 20)
    .reverse() 
    .map(m => {
        const direction = String(m.direction || '').toLowerCase();
        const isOutbound = ['outbound', 'sent', 'out'].includes(direction);
        const prefix = isOutbound ? 'Emerson (Você): ' : 'Cliente: ';
        return `${prefix}${m.message}`;
    })
    .join('\\n');

return [{ json: { historico_recente: finalHistory || "Sem histórico relevante." } }];
"""
            primeiro['parameters']['jsCode'] = new_code
            print("Updated Formatar Historico JS code and removed duplicates.")

    # Recurse
    for key, value in obj.items():
        if isinstance(value, dict):
            fix_history_nodes(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    fix_history_nodes(item)

fix_history_nodes(data)

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("History fix complete.")
