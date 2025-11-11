import requests
import time

API_BASE = "http://127.0.0.1:8000"

print("🧪 Testing System Performance\n")

# Test 1: Quick dashboard
print("1️⃣ Testing quick dashboard...")
start = time.time()
response = requests.get(f"{API_BASE}/dashboard-quick")
elapsed = time.time() - start
print(f"✅ Quick dashboard: {elapsed:.2f}s")
print(f"   Records: {response.json()['total_records']}\n")

# Test 2: Verify all (limit 5)
print("2️⃣ Testing verification (limit 5)...")
start = time.time()
response = requests.get(f"{API_BASE}/verify-all?limit=5")
elapsed = time.time() - start
data = response.json()
print(f"✅ Verification: {elapsed:.2f}s")
print(f"   Verified: {data['verified']}")
print(f"   Tampered: {data['tampered']}\n")

# Test 3: Clear cache
print("3️⃣ Clearing cache...")
requests.post(f"{API_BASE}/cache/clear")
print("✅ Cache cleared\n")

print("✅ All tests complete!")
