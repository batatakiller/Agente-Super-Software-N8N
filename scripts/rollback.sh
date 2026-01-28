#!/bin/bash

# Configuration
API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMWU0ZDc4Mi0yYzcxLTQyMDctOWMyNS1kYThhOTUwNDkxYjEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5NTI2NDE4fQ.U8Ha2CKa7E_CJBBe1THhEs4fTCI3rv3pkwLO4KluVCw"
WORKFLOW_ID="H5Ti5RcPjjoWFUZS"
BASE_URL="https://n8n.supersoftware.info/api/v1"
FILE="Agente SuperSoftware.json"
TEMP_FILE="temp_workflow_rollback.json"

echo "⏪ Iniciando rollback do workflow..."

# 1. Revert local file using git
if ! git checkout HEAD^ -- "$FILE"; then
    echo "❌ Erro ao recuperar versão anterior do Git. Você já fez um commit?"
    exit 1
fi

echo "✅ Arquivo local restaurado para a versão anterior."

# 2. Clean JSON of the reverted file
jq '{name, nodes, connections, settings}' "$FILE" > "$TEMP_FILE"

# 3. Deploy the reverted version
echo "📤 Enviando versão restaurada para o n8n..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/workflows/$WORKFLOW_ID" \
     -H "X-N8N-API-KEY: $API_KEY" \
     -H "Content-Type: application/json" \
     --data-binary @"$TEMP_FILE")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Rollback concluído com sucesso no n8n!"
    rm "$TEMP_FILE"
else
    echo "❌ Erro ao fazer deploy da versão de rollback (HTTP $HTTP_CODE)."
    rm "$TEMP_FILE"
    exit 1
fi
