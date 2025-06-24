-- Enable pgvector extension for similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Create custom types for IDs
CREATE DOMAIN user_id_type AS TEXT CHECK (VALUE ~ '^user_[a-z0-9]{25}$');
CREATE DOMAIN account_id_type AS TEXT CHECK (VALUE ~ '^acc_[a-z0-9]{25}$');
CREATE DOMAIN transaction_id_type AS TEXT CHECK (VALUE ~ '^trans_[a-z0-9]{25}$');

-- Users table
CREATE TABLE users (
    id user_id_type UNIQUE,
    name VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    akahu_id VARCHAR(255) UNIQUE,
    auth_token TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (id, name)
);

-- Accounts table
CREATE TABLE accounts (
    id account_id_type PRIMARY KEY,
    user_id user_id_type NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255),
    company VARCHAR(255),
    amount DECIMAL(15,2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Segments table
CREATE TABLE segments (
    id SERIAL PRIMARY KEY,
    user_id user_id_type NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    colour VARCHAR(7),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, name)
);

-- Models table for ML models
CREATE TABLE models (
    name VARCHAR(255) PRIMARY KEY,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transactions table
CREATE TABLE transactions (
    id transaction_id_type PRIMARY KEY,
    account account_id_type NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    user_id user_id_type NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    hash TEXT,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    type VARCHAR(255),
    amount DECIMAL(12,2) NOT NULL,
    description TEXT,
    category VARCHAR(255),
    group_name VARCHAR(255),
    merchant VARCHAR(255),
    segment_id INTEGER REFERENCES segments(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Embeddings table with vector support
CREATE TABLE embeddings (
    hash TEXT PRIMARY KEY,
    embedding vector(768) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Assignments table (linking transactions to segments)
CREATE TABLE assignments (
    user_id user_id_type NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    hash TEXT NOT NULL,
    segment_id INTEGER REFERENCES segments(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, hash)
);

-- prediction table for ML predictions
CREATE TABLE predictions (
    user_id user_id_type NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    model SERIAL REFERENCES models(id) ON DELETE CASCADE
    hash TEXT NOT NULL,
    prediction INTEGER REFERENCES segments(id) ON DELETE CASCADE,
    confidence DECIMAL(5,4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, hash)
);

-- Ignored transactions table
CREATE TABLE ignored (
    id SERIAL PRIMARY KEY,
    transaction_id transaction_id_type NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_account ON transactions(account);
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_hash ON transactions(hash);
CREATE INDEX idx_transactions_segment_id ON transactions(segment_id);

CREATE INDEX idx_accounts_user_id ON accounts(user_id);
CREATE INDEX idx_segments_user_id ON segments(user_id);
CREATE INDEX idx_assignments_user_id ON assignments(user_id);
CREATE INDEX idx_assignments_segment_id ON assignments(segment_id);
CREATE INDEX idx_prediction_user_id ON predictions(user_id);
CREATE INDEX idx_prediction_segment_id ON predictions(prediction);

-- Vector similarity search indexes
-- HNSW index for fast approximate similarity search
CREATE INDEX idx_embeddings_hnsw ON embeddings USING hnsw (embedding vector_cosine_ops);
-- IVFFlat index alternative (you can choose one based on your needs)
-- CREATE INDEX idx_embeddings_ivfflat ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Update timestamp triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_accounts_updated_at BEFORE UPDATE ON accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_segments_updated_at BEFORE UPDATE ON segments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_models_updated_at BEFORE UPDATE ON models
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_transactions_updated_at BEFORE UPDATE ON transactions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Sample queries for similarity search
-- Find similar embeddings using cosine similarity
-- SELECT hash, embedding <=> '[0.1,0.2,0.3,...]'::vector AS distance 
-- FROM embeddings 
-- ORDER BY embedding <=> '[0.1,0.2,0.3,...]'::vector 
-- LIMIT 10;

-- Find similar embeddings using dot product
-- SELECT hash, (embedding <#> '[0.1,0.2,0.3,...]'::vector) * -1 AS similarity 
-- FROM embeddings 
-- ORDER BY embedding <#> '[0.1,0.2,0.3,...]'::vector 
-- LIMIT 10;