import psycopg2
import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Database configuration - Neon
DATABASE_URL = os.getenv("DATABASE_URL")

# CSV output path
CSV_PATH = "Database/employees_live.csv"

def export_to_csv():
    """Export secure_db table to CSV file"""
    try:
        # Connect to Neon database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Fetch all records
        cursor.execute("SELECT * FROM secure_db ORDER BY id;")
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'secure_db' 
            ORDER BY ordinal_position;
        """)
        columns = [row[0] for row in cursor.fetchall()]
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=columns)
        
        # Export to CSV
        df.to_csv(CSV_PATH, index=False)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ✅ Exported {len(rows)} records to {CSV_PATH}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")
        return False

def continuous_export(interval_seconds=10):
    """Continuously export database to CSV at regular intervals"""
    print(f"🔄 Starting continuous CSV export (every {interval_seconds} seconds)...")
    print(f"📁 Output file: {CSV_PATH}")
    print("Press Ctrl+C to stop.\n")
    
    try:
        while True:
            export_to_csv()
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n⏹️  Export stopped by user.")

if __name__ == "__main__":
    # Create Database folder if it doesn't exist
    os.makedirs("Database", exist_ok=True)
    
    # Run continuous export (every 10 seconds)
    continuous_export(interval_seconds=10)
