-- Neon PostgreSQL Setup Script
-- Run this with: psql 'postgresql://neondb_owner:npg_YFqTmsx8vwc9@ep-tiny-poetry-ahhtzm5d-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require'

-- Drop table if exists
DROP TABLE IF EXISTS secure_db;

-- Create the secure_db table
CREATE TABLE IF NOT EXISTS secure_db (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT,
    salary TEXT,
    record_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_name ON secure_db(name);
CREATE INDEX IF NOT EXISTS idx_created_at ON secure_db(created_at);

-- Insert sample data (optional)
INSERT INTO secure_db (name, role, salary) 
VALUES 
    ('Alice', 'Engineer', '70000'),
    ('Bob', 'Manager', '80000'),
    ('Charlie', 'Developer', '65000');

-- Verify
SELECT * FROM secure_db ORDER BY id;
