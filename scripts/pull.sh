#!/bin/bash

# Configuration
API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMWU0ZDc4Mi0yYzcxLTQyMDctOWMyNS1kYThhOTUwNDkxYjEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5NTI2NDE4fQ.U8Ha2CKa7E_CJBBe1THhEs4fTCI3rv3pkwLO4KluVCw"
WORKFLOW_ID="H5Ti5RcPjjoWFUZS"
BASE_URL="https://n8n.supersoftware.info/api/v1"
FILE="Agente SuperSoftware.json"

echo "📥 Baixando workflow atualizado do n8n: $WORKFLOW_ID..."

# 1. Fetch via API
RESPONSE=$(curl -s -H "X-N8N-API-KEY: $API_KEY" "$BASE_URL/workflows/$WORKFLOW_ID")

if [ -z "$RESPONSE" ]; then
    echo "❌ Erro ao buscar o workflow. Resposta vazia."
    exit 1
fi

# 2. Save and format with jq
if echo "$RESPONSE" | jq '.' > "$FILE"; then
    echo "✅ Workflow salvo com sucesso em $FILE"
else
    echo "❌ Erro ao processar o JSON recebido. Verifique a resposta da API."
    echo "$RESPONSE" | head -n 20
    exit 1
fi
