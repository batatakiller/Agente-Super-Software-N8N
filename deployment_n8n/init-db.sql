-- n8n_fila_mensagens
CREATE TABLE IF NOT EXISTS n8n_fila_mensagens (
    id SERIAL PRIMARY KEY,
    id_mensagem VARCHAR(255) NOT NULL,
    telefone VARCHAR(50) NOT NULL,
    mensagem TEXT,
    timestamp TIMESTAMP
    WITH
        TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- n8n_historico_mensagens
CREATE TABLE IF NOT EXISTS n8n_historico_mensagens (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    message JSONB NOT NULL
);

-- contacts
CREATE TABLE IF NOT EXISTS contacts (
    phone VARCHAR(50) PRIMARY KEY,
    ai_paused BOOLEAN DEFAULT FALSE,
    last_human_interaction TIMESTAMP
    WITH
        TIME ZONE DEFAULT CURRENT_TIMESTAMP
);