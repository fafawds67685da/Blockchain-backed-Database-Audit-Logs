from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
import hashlib
from datetime import datetime
import os
from dotenv import load_dotenv
import sys
import io
import csv
from fpdf import FPDF
import asyncio
from functools import lru_cache
from time import time

sys.path.append('..')
from blockchain_client import push_hash, fetch_hash, w3
from email_notifier import send_tampering_alert

load_dotenv()

app = FastAPI(title="Blockchain Audit API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_db():
    """Get PostgreSQL connection with timeout - supports Neon cloud DB"""
    try:
        # Check if we're using Neon (cloud) or local PostgreSQL
        db_host = os.getenv("DB_HOST", "localhost")
        is_neon = "neon.tech" in db_host
        
        if is_neon:
            # Neon PostgreSQL requires SSL
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME", "neondb"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD"),
                host=db_host,
                port=os.getenv("DB_PORT", 5432),
                sslmode='require',
                connect_timeout=10
            )
        else:
            # Local PostgreSQL
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME", "audit_logs"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD"),
                host=db_host,
                port=os.getenv("DB_PORT", 5432),
                connect_timeout=5
            )
        
        return conn
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

# Models
class Employee(BaseModel):
    id: int  # User must provide ID
    name: str
    role: str
    salary: str
    force_duplicate: bool = False

class EmployeeResponse(BaseModel):
    id: int
    name: str
    role: str
    salary: str
    record_hash: str
    created_at: datetime
    tx_hash: Optional[str] = None

class VerificationResult(BaseModel):
    id: int
    name: str
    role: str
    salary: str
    is_tampered: bool
    stored_hash: str
    computed_hash: str
    blockchain_hash: str
    created_at: datetime

class SearchFilter(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None

class TamperRequest(BaseModel):
    employee_id: int
    field: str
    new_value: str

# Transaction history
transaction_history = []

@app.get("/")
def root():
    return {
        "message": "Blockchain Audit API v2.0",
        "status": "operational"
    }

@app.get("/employees/check-duplicate/{name}")
def check_duplicate_name(name: str):
    """Check if employee name already exists"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, role FROM secure_db WHERE LOWER(name) = LOWER(%s);", (name,))
        existing = cursor.fetchall()
        
        cursor.close()
        
        if existing:
            return {
                "exists": True,
                "count": len(existing),
                "employees": [{"id": row[0], "name": row[1], "role": row[2]} for row in existing]
            }
        else:
            return {"exists": False, "count": 0, "employees": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.post("/employees", response_model=EmployeeResponse)
async def create_employee(employee: Employee, background_tasks: BackgroundTasks):
    """Create new employee with manual ID and push hash to blockchain"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if ID already exists
        cursor.execute("SELECT id FROM secure_db WHERE id = %s;", (employee.id,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(
                status_code=409,
                detail=f"Employee ID {employee.id} already exists. Please choose a different ID."
            )
        
        # Check for duplicate names if not forcing
        if not employee.force_duplicate:
            cursor.execute("SELECT id, name FROM secure_db WHERE LOWER(name) = LOWER(%s);", (employee.name,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.close()
                conn.close()
                raise HTTPException(
                    status_code=409,
                    detail=f"Employee with name '{employee.name}' already exists (ID: {existing[0]}). Set force_duplicate=true to override."
                )
        
        timestamp = datetime.now().isoformat()
        data_to_hash = f"{employee.name}{employee.role}{employee.salary}{timestamp}".encode('utf-8')
        record_hash = hashlib.sha256(data_to_hash).hexdigest()
        
        cursor.execute("""
            INSERT INTO secure_db (id, name, role, salary, record_hash, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, name, role, salary, record_hash, created_at;
        """, (employee.id, employee.name, employee.role, employee.salary, record_hash, timestamp))
        
        result = cursor.fetchone()
        employee_id = result[0]
        conn.commit()
        cursor.close()
        
        # Push to blockchain in background
        background_tasks.add_task(push_hash_to_blockchain, employee_id, employee.name, record_hash, timestamp)
        
        return {
            "id": result[0],
            "name": result[1],
            "role": result[2],
            "salary": result[3],
            "record_hash": result[4],
            "created_at": result[5],
            "tx_hash": "pending"
        }
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

def push_hash_to_blockchain(employee_id, employee_name, record_hash, timestamp):
    """Background task to push hash to blockchain"""
    try:
        receipt = push_hash(employee_id, record_hash)
        tx_hash = receipt['transactionHash'].hex() if receipt else None
        
        transaction_history.append({
            "tx_hash": tx_hash,
            "employee_name": employee_name,
            "employee_id": employee_id,
            "record_hash": record_hash,
            "timestamp": timestamp,
            "etherscan_link": f"https://sepolia.etherscan.io/tx/{tx_hash}" if tx_hash else None
        })
    except Exception as e:
        print(f"Failed to push to blockchain: {e}")

@app.get("/employees", response_model=List[EmployeeResponse])
def get_all_employees():
    """Get all employees - optimized without blockchain calls"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, role, salary, record_hash, created_at FROM secure_db ORDER BY id;")
        rows = cursor.fetchall()
        
        cursor.close()
        
        return [
            {
                "id": row[0],
                "name": row[1],
                "role": row[2],
                "salary": row[3],
                "record_hash": row[4],
                "created_at": row[5],
                "tx_hash": None  # Don't fetch tx_hash for list view (performance)
            }
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.post("/employees/search")
def search_employees(filters: SearchFilter):
    """Search and filter employees"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        query = "SELECT id, name, role, salary, record_hash, created_at FROM secure_db WHERE 1=1"
        params = []
        
        if filters.name:
            query += " AND LOWER(name) LIKE LOWER(%s)"
            params.append(f"%{filters.name}%")
        
        if filters.role:
            query += " AND LOWER(role) LIKE LOWER(%s)"
            params.append(f"%{filters.role}%")
        
        if filters.min_salary:
            query += " AND CAST(salary AS FLOAT) >= %s"
            params.append(filters.min_salary)
        
        if filters.max_salary:
            query += " AND CAST(salary AS FLOAT) <= %s"
            params.append(filters.max_salary)
        
        query += " ORDER BY id;"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        cursor.close()
        
        return [
            {
                "id": row[0],
                "name": row[1],
                "role": row[2],
                "salary": row[3],
                "record_hash": row[4],
                "created_at": row[5]
            }
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.get("/employees/{employee_id}/verify", response_model=VerificationResult)
async def verify_employee(employee_id: int, background_tasks: BackgroundTasks):
    """Verify integrity of a single employee"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, role, salary, record_hash, created_at 
            FROM secure_db WHERE id = %s;
        """, (employee_id,))
        
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        emp_id, name, role, salary, stored_hash, created_at = row
        combined_data = f"{name}{role}{salary}{created_at.isoformat()}".encode('utf-8')
        computed_hash = hashlib.sha256(combined_data).hexdigest()
        
        # Fetch from blockchain (can be slow, but necessary)
        try:
            blockchain_hash = fetch_hash(emp_id)
        except:
            blockchain_hash = "0" * 64  # Fallback if blockchain fails
        
        is_tampered = not (stored_hash == computed_hash == blockchain_hash)
        
        # Send email alert in background
        if is_tampered:
            background_tasks.add_task(
                send_tampering_alert,
                name, emp_id, stored_hash, computed_hash, blockchain_hash
            )
        
        return {
            "id": emp_id,
            "name": name,
            "role": role,
            "salary": salary,
            "is_tampered": is_tampered,
            "stored_hash": stored_hash,
            "computed_hash": computed_hash,
            "blockchain_hash": blockchain_hash,
            "created_at": created_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.get("/dashboard-quick")
def get_dashboard_quick():
    """Fast dashboard - just shows database records without blockchain verification"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM secure_db;")
        total_records = cursor.fetchone()[0]
        
        cursor.execute("SELECT id, name, role, salary, created_at FROM secure_db ORDER BY created_at DESC LIMIT 20;")
        records = cursor.fetchall()
        
        cursor.close()
        
        return {
            "total_records": total_records,
            "records": [
                {
                    "id": row[0],
                    "name": row[1],
                    "role": row[2],
                    "salary": row[3],
                    "created_at": row[4]
                }
                for row in records
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

# Add cache for blockchain hashes (TTL: 5 minutes)
blockchain_cache = {}
CACHE_TTL = 300  # 5 minutes

def fetch_hash_cached(employee_id: int) -> str:
    """Fetch hash from blockchain with caching"""
    current_time = time()
    cache_key = f"hash_{employee_id}"
    
    # Check cache
    if cache_key in blockchain_cache:
        cached_data, cached_time = blockchain_cache[cache_key]
        if current_time - cached_time < CACHE_TTL:
            return cached_data
    
    # Fetch from blockchain
    try:
        hash_value = fetch_hash(employee_id)
        blockchain_cache[cache_key] = (hash_value, current_time)
        return hash_value
    except Exception as e:
        print(f"❌ Error fetching hash for ID {employee_id}: {e}")
        return "0" * 64

@app.get("/verify-all")
async def verify_all_employees(background_tasks: BackgroundTasks, limit: int = 10):
    """Verify employees - limit to prevent timeout"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get total count first
        cursor.execute("SELECT COUNT(*) FROM secure_db;")
        total_in_db = cursor.fetchone()[0]
        
        # Only verify limited records
        cursor.execute(f"SELECT id, name, role, salary, record_hash, created_at FROM secure_db ORDER BY id LIMIT {limit};")
        rows = cursor.fetchall()
        
        cursor.close()
        
        results = []
        tampered_count = 0
        verified_count = 0
        
        for row in rows:
            try:
                emp_id, name, role, salary, stored_hash, created_at = row
                
                if not stored_hash or not created_at:
                    continue
                
                combined_data = f"{name}{role}{salary}{created_at.isoformat()}".encode('utf-8')
                computed_hash = hashlib.sha256(combined_data).hexdigest()
                
                # Use cached fetch
                blockchain_hash = fetch_hash_cached(emp_id)
                
                is_tampered = not (stored_hash == computed_hash == blockchain_hash)
                
                if is_tampered and blockchain_hash != "0" * 64:
                    tampered_count += 1
                    try:
                        background_tasks.add_task(
                            send_tampering_alert,
                            name, emp_id, stored_hash, computed_hash, blockchain_hash
                        )
                    except:
                        pass
                else:
                    verified_count += 1
                
                results.append({
                    "id": emp_id,
                    "name": name,
                    "role": role,
                    "salary": salary,
                    "is_tampered": is_tampered,
                    "stored_hash": stored_hash,
                    "computed_hash": computed_hash,
                    "blockchain_hash": blockchain_hash,
                    "created_at": created_at
                })
                
            except Exception as row_error:
                print(f"❌ Error processing row: {row_error}")
                continue
        
        return {
            "total_records": total_in_db,
            "verified": verified_count,
            "tampered": tampered_count,
            "results": results
        }
    except Exception as e:
        print(f"❌ Critical error in verify-all: {e}")
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
    finally:
        if conn:
            conn.close()

@app.post("/cache/clear")
def clear_cache():
    """Clear blockchain hash cache"""
    global blockchain_cache
    blockchain_cache = {}
    return {"message": "Cache cleared", "timestamp": time()}

@app.post("/tamper")
def simulate_tampering(req: TamperRequest):
    """Simulate tampering - update any field"""
    conn = None
    try:
        # Validate field
        allowed_fields = ['name', 'role', 'salary']
        if req.field not in allowed_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid field. Allowed: {', '.join(allowed_fields)}"
            )
        
        conn = get_db()
        cursor = conn.cursor()
        
        sql = f'UPDATE secure_db SET "{req.field}" = %s WHERE id = %s RETURNING id, name, role, salary;'
        cursor.execute(sql, (req.new_value, req.employee_id))
        result = cursor.fetchone()
        conn.commit()
        
        cursor.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {
            "message": "Data tampered successfully (for demo)",
            "employee_id": result[0],
            "name": result[1],
            "role": result[2],
            "salary": result[3],
            "updated_field": req.field,
            "new_value": req.new_value
        }
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    """Delete an employee"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM secure_db WHERE id = %s RETURNING id, name;", (employee_id,))
        result = cursor.fetchone()
        conn.commit()
        
        cursor.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {"message": f"Employee {result[1]} (ID: {result[0]}) deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.delete("/employees/all/truncate")
def delete_all_employees():
    """Delete all employees (truncate table)"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM secure_db;")
        count = cursor.fetchone()[0]
        
        cursor.execute("TRUNCATE TABLE secure_db RESTART IDENTITY CASCADE;")
        conn.commit()
        
        cursor.close()
        
        return {"message": f"All {count} employee records deleted successfully", "deleted_count": count}
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.get("/transactions")
def get_transaction_history():
    """Get blockchain transaction history"""
    return {
        "total_transactions": len(transaction_history),
        "transactions": transaction_history[-20:]
    }

@app.get("/gas-stats")
def get_gas_statistics():
    """Get gas fee statistics"""
    try:
        gas_price = w3.eth.gas_price
        gas_price_gwei = w3.from_wei(gas_price, 'gwei')
        
        return {
            "current_gas_price_wei": gas_price,
            "current_gas_price_gwei": float(gas_price_gwei),
            "estimated_cost_per_transaction": {
                "gas_used": 200000,
                "cost_wei": gas_price * 200000,
                "cost_eth": float(w3.from_wei(gas_price * 200000, 'ether'))
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export/csv")
def export_csv():
    """Export all employees to CSV"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, role, salary, record_hash, created_at FROM secure_db ORDER BY id;")
        rows = cursor.fetchall()
        
        cursor.close()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Name', 'Role', 'Salary', 'Record Hash', 'Created At'])
        writer.writerows(rows)
        
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.get("/export/pdf")
def export_pdf():
    """Export verification report as PDF"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, role, salary FROM secure_db ORDER BY id LIMIT 50;")
        rows = cursor.fetchall()
        
        cursor.close()
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Blockchain Audit Report", 0, 1, 'C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(20, 10, "ID", 1)
        pdf.cell(50, 10, "Name", 1)
        pdf.cell(50, 10, "Role", 1)
        pdf.cell(40, 10, "Salary", 1)
        pdf.ln()
        
        pdf.set_font("Arial", '', 10)
        for row in rows:
            pdf.cell(20, 10, str(row[0]), 1)
            pdf.cell(50, 10, str(row[1])[:20], 1)
            pdf.cell(50, 10, str(row[2])[:20], 1)
            pdf.cell(40, 10, str(row[3]), 1)
            pdf.ln()
        
        pdf_output = pdf.output(dest='S').encode('latin1')
        
        return StreamingResponse(
            io.BytesIO(pdf_output),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
