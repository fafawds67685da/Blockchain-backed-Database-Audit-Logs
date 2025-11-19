import psycopg2
import hashlib
from datetime import datetime
from Others.blockchain_client import push_hash, fetch_hash

# ✅ Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="audit_logs",
    user="postgres",
    password="devsidhu@59",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# ✅ Drop and recreate table to ensure correct schema
cursor.execute("DROP TABLE IF EXISTS secure_db;")
cursor.execute("""
CREATE TABLE IF NOT EXISTS secure_db (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT,
    salary TEXT,
    record_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

def add_employee(name, role, salary):
    """Add new employee and push its hash to blockchain"""
    timestamp = datetime.now().isoformat()  # Current timestamp

    # Compute hash including timestamp (without employee_id, as it's auto-generated)
    data_to_hash = f"{name}{role}{salary}{timestamp}".encode('utf-8')
    record_hash = hashlib.sha256(data_to_hash).hexdigest()

    # Insert into DB and return the generated ID
    cursor.execute("""
        INSERT INTO secure_db (name, role, salary, record_hash, created_at)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (name, role, salary, record_hash, timestamp)
    )
    employee_id = cursor.fetchone()[0]
    conn.commit()

    # Push hash to blockchain using employee ID
    push_hash(name, record_hash)
    print(f"✅ Employee {name} (ID: {employee_id}) added successfully with hash:\n   {record_hash}")


def verify_integrity(employee_id):
    """Verify integrity of employee by ID"""
    cursor.execute("SELECT id, name, role, salary, record_hash, created_at FROM secure_db WHERE id = %s;", (employee_id,))
    row = cursor.fetchone()

    if not row:
        print("❌ Employee not found in database.")
        return

    emp_id, name, role, salary, stored_hash, created_at = row
    combined_data = f"{name}{role}{salary}{created_at.isoformat()}".encode('utf-8')
    computed_hash = hashlib.sha256(combined_data).hexdigest()

    blockchain_hash = fetch_hash(name)

    print("\n🧾 Current Record:")
    print(f"   ID: {emp_id}")
    print(f"   Name: {name}")
    print(f"   Role: {role}")
    print(f"   Salary: {salary}")
    print(f"   Timestamp: {created_at}")
    print(f"\n📊 Hash Comparison:")
    print(f"   🔍 Stored DB Hash:     {stored_hash}")
    print(f"   🔄 Recomputed Hash:    {computed_hash}")
    print(f"   ⛓️  Blockchain Hash:    {blockchain_hash}\n")

    # Check all three hashes
    if stored_hash == computed_hash == blockchain_hash:
        print("✅ Integrity Verified — Record is Untampered.")
        print("   All hashes match: Data has not been modified.\n")
    elif stored_hash == blockchain_hash and computed_hash != stored_hash:
        print("⚠️  ALERT: Data Tampering Detected!")
        print("   The data in the database has been modified after initial storage.")
        print(f"   Original data hash: {stored_hash}")
        print(f"   Current data hash:  {computed_hash}")
        print("   The blockchain proves this record has been tampered with.\n")
    else:
        print("⚠️  CRITICAL: Hash inconsistency detected!")
        print("   Stored hash and blockchain hash don't match.")
        print("   This may indicate database corruption or blockchain sync issues.\n")


# === 🧠 Interactive Menu ===
def main():
    print("\n=== 🔒 Blockchain-Backed Audit Database ===")
    print("1️⃣  Add new employee record")
    print("2️⃣  Verify integrity of an employee")
    print("3️⃣  Exit")

    while True:
        choice = input("\nEnter your choice (1/2/3): ").strip()
        if choice == "1":
            name = input("Enter employee name: ").strip()
            role = input("Enter employee role: ").strip()
            salary = input("Enter employee salary: ").strip()
            add_employee(name, role, salary)
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
