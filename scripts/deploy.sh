#!/bin/bash

# Configuration
API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMWU0ZDc4Mi0yYzcxLTQyMDctOWMyNS1kYThhOTUwNDkxYjEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5NTI2NDE4fQ.U8Ha2CKa7E_CJBBe1THhEs4fTCI3rv3pkwLO4KluVCw"
WORKFLOW_ID="H5Ti5RcPjjoWFUZS"
BASE_URL="https://n8n.supersoftware.info/api/v1"
FILE="Agente SuperSoftware.json"
TEMP_FILE="temp_workflow_deploy.json"

echo "🚀 Iniciando deploy do workflow: $FILE..."

# 1. Clean JSON
if ! jq '{name, nodes, connections, settings}' "$FILE" > "$TEMP_FILE"; then
    echo "❌ Erro ao limpar o JSON. Verifique se o arquivo é um JSON válido."
    exit 1
fi

# 2. Deploy via API
echo "📤 Enviando para o n8n ($WORKFLOW_ID)..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/workflows/$WORKFLOW_ID" \
     -H "X-N8N-API-KEY: $API_KEY" \
     -H "Content-Type: application/json" \
     --data-binary @"$TEMP_FILE")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Deploy concluído com sucesso!"
    rm "$TEMP_FILE"
else
    echo "❌ Er de deploy (HTTP $HTTP_CODE):"
    echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
    rm "$TEMP_FILE"
    exit 1
fi
