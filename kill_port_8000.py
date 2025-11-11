import os
import subprocess

print("🔍 Finding processes using port 8000...")

try:
    # Find process using port 8000
    result = subprocess.run(
        ['netstat', '-ano'],
        capture_output=True,
        text=True
    )
    
    for line in result.stdout.split('\n'):
        if ':8000' in line and 'LISTENING' in line:
            parts = line.split()
            pid = parts[-1]
            print(f"Found process using port 8000: PID {pid}")
            
            # Kill the process
            os.system(f'taskkill /PID {pid} /F')
            print(f"✅ Killed process {pid}")
            break
    else:
        print("ℹ️ No process found using port 8000")
        
except Exception as e:
    print(f"❌ Error: {e}")
