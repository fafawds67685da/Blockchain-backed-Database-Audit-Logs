import psycopg2
import hashlib
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

# ✅ Create table if not exists (no record_hash)
cursor.execute("""
CREATE TABLE IF NOT EXISTS secure_db (
    name TEXT PRIMARY KEY,
    role TEXT,
    salary TEXT
);
""")
conn.commit()


def add_employee(name, role, salary):
    """Add new employee and push its hash to blockchain"""
    # Compute hash (this will go only to blockchain)
    data_to_hash = f"{name}{role}{salary}".encode('utf-8')
    record_hash = hashlib.sha256(data_to_hash).hexdigest()

    # Insert into DB (no record_hash column now)
    cursor.execute(
        """
        INSERT INTO secure_db (name, role, salary)
        VALUES (%s, %s, %s)
        ON CONFLICT (name) DO UPDATE
        SET role = EXCLUDED.role, salary = EXCLUDED.salary;
        """,
        (name, role, salary)
    )
    conn.commit()

    # Push hash to blockchain
    push_hash(name, record_hash)
    print(f"✅ Employee {name} added successfully with hash:\n   {record_hash}")


def verify_integrity(name):
    """Recompute hash from DB values and verify against blockchain hash"""
    cursor.execute("SELECT name, role, salary FROM secure_db WHERE name = %s;", (name,))
    row = cursor.fetchone()

    if not row:
        print("❌ Employee not found in database.")
        return

    # Recompute hash from DB data
    name, role, salary = row
    combined_data = f"{name}{role}{salary}".encode('utf-8')
    new_hash = hashlib.sha256(combined_data).hexdigest()

    # Fetch blockchain hash
    blockchain_hash = fetch_hash(name)

    print("\n🧾 Current Record:")
    print(f"   Name: {name}")
    print(f"   Role: {role}")
    print(f"   Salary: {salary}")
    print(f"\n🔍 Recomputed DB Hash: {new_hash}")
    print(f"⛓  Blockchain Hash:    {blockchain_hash}\n")

    if new_hash == blockchain_hash:
        print("✅ Integrity Verified — Record is Untampered.")
    else:
        print("⚠️  ALERT: Data Tampering Detected!")
        print("   Blockchain hash does NOT match current DB values.")


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
            name = input("Enter employee name to verify: ").strip()
            verify_integrity(name)
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
