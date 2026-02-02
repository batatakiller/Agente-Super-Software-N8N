import re

filepath = 'Agente SuperSoftware.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = f.read()

# Replace $(...).item.json with $(...).first().json
# Handles 'Info', "Info", and escaped versions
data = re.sub(r"\$\((['\"]|\\+['\"])(.+?)\1\)\.item\.json", r"$([\1\2\1]).first().json", data)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(data)

print("Replaced node reference .item.json with .first().json")
