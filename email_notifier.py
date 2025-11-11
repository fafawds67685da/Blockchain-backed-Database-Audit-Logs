import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

def send_tampering_alert(employee_name, employee_id, stored_hash, computed_hash, blockchain_hash):
    """Send email alert when tampering is detected"""
    
    # Skip if email not configured
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECIPIENT:
        print(f"⚠️ Email not configured. Skipping alert for {employee_name}")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = f"🚨 DATA TAMPERING DETECTED - Employee {employee_name}"
        
        # Safe string conversion
        stored_str = str(stored_hash) if stored_hash else "N/A"
        computed_str = str(computed_hash) if computed_hash else "N/A"
        blockchain_str = str(blockchain_hash) if blockchain_hash else "N/A"
        
        body = f"""
        <html>
        <body>
            <h2 style="color: red;">⚠️ TAMPERING ALERT</h2>
            <p>Data tampering has been detected in the audit database.</p>
            
            <h3>Employee Details:</h3>
            <ul>
                <li><b>Name:</b> {employee_name}</li>
                <li><b>ID:</b> {employee_id}</li>
                <li><b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            
            <h3>Hash Verification:</h3>
            <ul>
                <li><b>Stored Hash:</b> <code>{stored_str[:32]}...</code></li>
                <li><b>Computed Hash:</b> <code style="color: red;">{computed_str[:32]}...</code></li>
                <li><b>Blockchain Hash:</b> <code>{blockchain_str[:32]}...</code></li>
            </ul>
            
            <p style="color: red; font-weight: bold;">
                The data has been modified after initial storage. 
                Immediate investigation required!
            </p>
            
            <hr>
            <p style="font-size: 12px; color: gray;">
                This is an automated alert from the Blockchain Audit System.
            </p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Alert email sent to {EMAIL_RECIPIENT}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
