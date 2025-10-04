import psycopg2
import hashlib

# --- Connect to database ---
conn = psycopg2.connect(
    dbname="audit_logs",
    user="postgres",
    password="devsidhu@59",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# --- Function to generate hash for a row ---
def generate_hash(id, name, role, salary):
    record_string = f"{id}|{name}|{role}|{salary}"
    return hashlib.sha256(record_string.encode()).hexdigest()

# --- 1. Generate hashes for rows without hash ---
cur.execute("SELECT id, name, role, salary FROM employees WHERE record_hash IS NULL;")
rows = cur.fetchall()

for row in rows:
    id, name, role, salary = row
    record_hash = generate_hash(id, name, role, salary)
    cur.execute(
        "UPDATE employees SET record_hash=%s WHERE id=%s;",
        (record_hash, id)
    )

conn.commit()
print("Hashes generated and stored successfully!")

# --- 2. Function to add a new employee with hash ---
def add_employee(name, role, salary):
    cur.execute(
        "INSERT INTO employees (name, role, salary) VALUES (%s, %s, %s) RETURNING id;",
        (name, role, salary)
    )
    new_id = cur.fetchone()[0]
    record_hash = generate_hash(new_id, name, role, salary)
    cur.execute(
        "UPDATE employees SET record_hash=%s WHERE id=%s;",
        (record_hash, new_id)
    )
    conn.commit()
    print(f"Added employee {name} with hash {record_hash}")

# Example: add a new employee
# add_employee("Bob Mehta", "Member 3", 55000)

# --- 3. Verify all rows ---
cur.execute("SELECT id, name, role, salary, record_hash FROM employees;")
all_rows = cur.fetchall()

for row in all_rows:
    id, name, role, salary, stored_hash = row
    calculated_hash = generate_hash(id, name, role, salary)
    if stored_hash == calculated_hash:
        print(f"Row {id} is authentic ✅")
    else:
        print(f"Row {id} has been tampered ❌")

cur.close()
conn.close()
