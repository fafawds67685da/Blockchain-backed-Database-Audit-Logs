-- Drop table if you want to recreate it
DROP TABLE IF EXISTS secure_db;

-- Create the secure_db table
CREATE TABLE IF NOT EXISTS secure_db (
    id SERIAL PRIMARY KEY,
    name TEXT,
    role TEXT,
    salary TEXT,
    record_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Example: Insert sample data
INSERT INTO secure_db (name, role, salary) VALUES ('Alice', 'Engineer', '70000');
INSERT INTO secure_db (name, role, salary) VALUES ('Bob', 'Manager', '80000');

-- Example: Update salary for a specific employee
UPDATE secure_db
SET salary = '45'
WHERE id = 1;

-- View all records
SELECT * FROM secure_db;