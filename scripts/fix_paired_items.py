import json

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = f.read()

# Replace both escaped and unescaped versions
# Note: n8n usually uses single quotes internally in expressions
# but they might be escaped in the JSON string.

data = data.replace("$('Info').item.json", "$('Info').first().json")
data = data.replace('$(\\"Info\\").item.json', '$(\\"Info\\").first().json')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(data)

print("Replaced all $('Info').item.json with $('Info').first().json")
