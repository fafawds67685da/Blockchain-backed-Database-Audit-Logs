import requests

API_BASE = "http://127.0.0.1:8000"

print("🧪 Testing Backend API with Neon Database\n")

# Test 1: Health check
print("1️⃣ Testing health endpoint...")
try:
    response = requests.get(f"{API_BASE}/", timeout=5)
    if response.status_code == 200:
        print(f"✅ Health check: {response.json()}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
except Exception as e:
    print(f"❌ Backend not running: {e}")
    print("💡 Start backend with: uvicorn backend.main:app --reload")
    exit(1)

# Test 2: Get all employees
print("\n2️⃣ Testing /employees endpoint...")
try:
    response = requests.get(f"{API_BASE}/employees", timeout=10)
    if response.status_code == 200:
        employees = response.json()
        print(f"✅ Found {len(employees)} employees")
        for emp in employees:
            print(f"   - {emp['name']} ({emp['role']}): ${emp['salary']}")
    else:
        print(f"❌ Failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Add new employee
print("\n3️⃣ Testing add employee...")
try:
    new_employee = {
        "name": "TestUser",
        "role": "Tester",
        "salary": "50000"
    }
    response = requests.post(f"{API_BASE}/employees", json=new_employee, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Employee added: ID {data['id']}, Hash: {data['record_hash'][:16]}...")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n✅ All tests completed!")
