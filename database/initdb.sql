-- Enable pgvector extension for similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Create custom types for IDs
CREATE DOMAIN user_id AS TEXT CHECK (VALUE ~ '^user_[a-z0-9]{25}$');
CREATE DOMAIN account_id AS TEXT CHECK (VALUE ~ '^acc_[a-z0-9]{25}$');
CREATE DOMAIN transaction_id AS TEXT CHECK (VALUE ~ '^trans_[a-z0-9]{25}$');

-- Users table
CREATE TABLE users (
    id user_id PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    akahu_id VARCHAR(255) UNIQUE,
    auth_token TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Accounts table
CREATE TABLE accounts (
    id account_id PRIMARY KEY,
    user_id user_id NOT NULL REFERENCES users(_id) ON DELETE CASCADE,
    company VARCHAR(255),
    amount DECIMAL(15,2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Segments table
CREATE TABLE segments (
    id SERIAL PRIMARY KEY,
    user_id user_id NOT NULL REFERENCES users(_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    colour VARCHAR(7),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(_user_id, name)
);

-- Models table for ML models
CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transactions table
CREATE TABLE transactions (
    id transaction_id PRIMARY KEY,
    account account_id NOT NULL REFERENCES accounts(_id) ON DELETE CASCADE,
    user_id user_id NOT NULL REFERENCES users(_id) ON DELETE CASCADE,
    hash TEXT,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    type VARCHAR(255),
    amount DECIMAL(12,2) NOT NULL,
    description TEXT,
    category VARCHAR(255),
    group_name VARCHAR(255),
    merchant VARCHAR(255),
    segment_id INTEGER REFERENCES segments(_id) ON DELETE SET NULL,
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
    user_id user_id NOT NULL REFERENCES users(_id) ON DELETE CASCADE,
    hash TEXT NOT NULL,
    segment_id INTEGER REFERENCES segments(_id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (_user_id, hash)
);

-- Classification table for ML predictions
CREATE TABLE classification (
    user_id user_id NOT NULL REFERENCES users(_id) ON DELETE CASCADE,
    hash TEXT NOT NULL,
    segment_id INTEGER REFERENCES segments(_id) ON DELETE CASCADE,
    prediction TEXT,
    confidence DECIMAL(5,4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (_user_id, hash)
);

-- Ignored transactions table
CREATE TABLE ignored (
    id SERIAL PRIMARY KEY,
    transaction_id transaction_id NOT NULL REFERENCES transactions(_id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_transactions_user_id ON transactions(_user_id);
CREATE INDEX idx_transactions_account ON transactions(_account);
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_hash ON transactions(hash);
CREATE INDEX idx_transactions_segment_id ON transactions(_segment_id);

CREATE INDEX idx_accounts_user_id ON accounts(_user_id);
CREATE INDEX idx_segments_user_id ON segments(_user_id);
CREATE INDEX idx_assignments_user_id ON assignments(_user_id);
CREATE INDEX idx_assignments_segment_id ON assignments(_segment_id);
CREATE INDEX idx_classification_user_id ON classification(_user_id);
CREATE INDEX idx_classification_segment_id ON classification(_segment_id);

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