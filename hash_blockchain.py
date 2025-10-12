import psycopg2
import hashlib
from datetime import datetime
from blockchain_client import push_hash, fetch_hash

# ✅ Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="audit_logs",
    user="postgres",
    password="devsidhu@59",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# ✅ Create table if not exists (employee_id is now manually provided)
cursor.execute("""
CREATE TABLE IF NOT EXISTS secure_db (
    employee_id INT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    role TEXT,
    salary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

def add_employee(employee_id, name, role, salary):
    """Add new employee and push its hash to blockchain"""
    timestamp = datetime.now().isoformat()  # Current timestamp

    # Compute hash including timestamp
    data_to_hash = f"{employee_id}{name}{role}{salary}{timestamp}".encode('utf-8')
    record_hash = hashlib.sha256(data_to_hash).hexdigest()

    # Insert into DB
    cursor.execute("""
        INSERT INTO secure_db (employee_id, name, role, salary, created_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (employee_id) DO UPDATE
        SET name = EXCLUDED.name, role = EXCLUDED.role, salary = EXCLUDED.salary, created_at = EXCLUDED.created_at;
        """,
        (employee_id, name, role, salary, timestamp)
    )
    conn.commit()

    # Push hash to blockchain
    push_hash(str(employee_id), record_hash)
    print(f"✅ Employee {name} (ID: {employee_id}) added successfully with hash:\n   {record_hash}")


def verify_integrity(employee_id):
    """Verify integrity of employee by ID"""
    cursor.execute("SELECT employee_id, name, role, salary, created_at FROM secure_db WHERE employee_id = %s;", (employee_id,))
    row = cursor.fetchone()

    if not row:
        print("❌ Employee not found in database.")
        return

    emp_id, name, role, salary, created_at = row
    combined_data = f"{emp_id}{name}{role}{salary}{created_at.isoformat()}".encode('utf-8')
    new_hash = hashlib.sha256(combined_data).hexdigest()

    blockchain_hash = fetch_hash(str(emp_id))

    print("\n🧾 Current Record:")
    print(f"   ID: {emp_id}")
    print(f"   Name: {name}")
    print(f"   Role: {role}")
    print(f"   Salary: {salary}")
    print(f"   Timestamp: {created_at}")
    print(f"\n🔍 Recomputed DB Hash: {new_hash}")
    print(f"⛓  Blockchain Hash:    {blockchain_hash}\n")

    if new_hash == blockchain_hash:
        print("✅ Integrity Verified — Record is Untampered.")
    else:
        print("⚠️  ALERT: Data Tampering Detected! Blockchain hash mismatch.")


# === 🧠 Interactive Menu ===
def main():
    print("\n=== 🔒 Blockchain-Backed Audit Database ===")
    print("1️⃣  Add new employee record")
    print("2️⃣  Verify integrity of an employee")
    print("3️⃣  Exit")

    while True:
        choice = input("\nEnter your choice (1/2/3): ").strip()
        if choice == "1":
            employee_id = int(input("Enter employee ID: ").strip())
            name = input("Enter employee name: ").strip()
            role = input("Enter employee role: ").strip()
            salary = input("Enter employee salary: ").strip()
            add_employee(employee_id, name, role, salary)
        elif choice == "2":
            employee_id = int(input("Enter employee ID to verify: ").strip())
            verify_integrity(employee_id)
        elif choice == "3":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    print("✅ Connected to Sepolia testnet")
    main()
    conn.close()
    print("👋 Goodbye!")
