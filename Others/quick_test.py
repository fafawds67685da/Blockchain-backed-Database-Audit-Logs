import requests
import time

API_BASE = "http://127.0.0.1:8000"

print("🧪 Quick System Test\n")

# Test 1: Backend Health
print("1️⃣ Testing backend health...")
try:
    response = requests.get(f"{API_BASE}/", timeout=5)
    if response.status_code == 200:
        print(f"✅ Backend is online")
        print(f"   Response: {response.json()}\n")
    else:
        print(f"❌ Backend returned status {response.status_code}\n")
except Exception as e:
    print(f"❌ Backend not responding: {e}")
    print(f"💡 Start backend with: cd backend && uvicorn main:app --reload\n")
    exit(1)

# Test 2: Get Employees
print("2️⃣ Testing /employees endpoint...")
try:
    response = requests.get(f"{API_BASE}/employees", timeout=10)
    if response.status_code == 200:
        employees = response.json()
        print(f"✅ Found {len(employees)} employees\n")
    else:
        print(f"❌ Failed with status {response.status_code}\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 3: Verify All
print("3️⃣ Testing verification...")
try:
    response = requests.get(f"{API_BASE}/verify-all", timeout=15)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Verification complete:")
        print(f"   Total: {data['total_records']}")
        print(f"   Verified: {data['verified']}")
        print(f"   Tampered: {data['tampered']}\n")
        
        if data['verified'] == data['total_records']:
            print("🎉 All records verified! System working perfectly!\n")
        else:
            print("⚠️  Some records show as tampered\n")
    else:
        print(f"❌ Failed with status {response.status_code}\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

print("✅ Test complete!")
print("\nNext steps:")
print("1. Open http://localhost:3000 in browser")
print("2. Click 'Refresh Dashboard'")
print("3. All 3 employees should show as verified!")
