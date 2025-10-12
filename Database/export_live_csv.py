import psycopg2
import pandas as pd
import time

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="audit_logs",
    user="postgres",
    password="devsidhu@59",
    host="localhost",
    port="5432"
)

csv_file = "D:/Blockchain-backed-Database-Audit-Logs/Database/employees_live.csv"

while True:
    # Fetch data from employees table
    df = pd.read_sql_query("SELECT * FROM secure_db", conn)
    
    # Write to CSV (overwrite each time)
    df.to_csv(csv_file, index=False)
    
    print(f"CSV updated! {len(df)} rows saved.")
    
    # Wait before next update (e.g., 10 seconds)
    time.sleep(10)
