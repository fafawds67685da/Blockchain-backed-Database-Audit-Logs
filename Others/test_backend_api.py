import requests
import json

API_BASE = "http://127.0.0.1:8000"

print("🧪 Testing Backend API\n")

# Test 1: Health Check
print("1️⃣ Health Check...")
try:
    response = requests.get(f"{API_BASE}/", timeout=5)
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 2: Get Employees
print("2️⃣ Get All Employees...")
try:
    response = requests.get(f"{API_BASE}/employees", timeout=10)
    print(f"✅ Status: {response.status_code}")
    employees = response.json()
    print(f"Found {len(employees)} employees:")
    for emp in employees:
        print(f"  - ID {emp['id']}: {emp['name']} ({emp['role']}) - ${emp['salary']}")
    print()
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 3: Add Employee
print("3️⃣ Add New Employee...")
try:
    new_emp = {
        "name": "TestUser",
        "role": "QA Engineer",
        "salary": "60000"
    }
    response = requests.post(f"{API_BASE}/employees", json=new_emp, timeout=10)
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Added: {data['name']} (ID: {data['id']})")
        print(f"Hash: {data['record_hash'][:32]}...")
        print(f"TX: {data.get('tx_hash', 'pending')}\n")
    else:
        print(f"Response: {response.text}\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 4: Verify Employee
print("4️⃣ Verify Employee...")
try:
    response = requests.get(f"{API_BASE}/employees/1/verify", timeout=10)
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Name: {data['name']}")
        print(f"Tampered: {data['is_tampered']}")
        print(f"Stored Hash: {data['stored_hash'][:32]}...")
        print(f"Computed Hash: {data['computed_hash'][:32]}...")
        print(f"Blockchain Hash: {data['blockchain_hash'][:32]}...\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

print("✅ All tests completed!")
