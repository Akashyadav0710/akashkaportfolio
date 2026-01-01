import sqlite3 # 1. Database library import ki
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- DATABASE SETUP FUNCTION ---
def init_db():
    # Ye function check karega ki table bani hai ya nahi, agar nahi to bana dega
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            company TEXT,
            service TEXT,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
# -------------------------------

@app.route('/')
def home():
    return render_template('skyy.html')

@app.route('/rumi')
def rumi():
    return render_template('rumi.html')

@app.route('/elite')
def elite():
    return render_template('elite.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Form se data nikaal rahe hain
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('tel')
        company = request.form.get('company')
        service = request.form.get('service')
        message = request.form.get('message')

        # --- DATABASE MEIN SAVE KARNA (INSERT QUERY) ---
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            # SQL Query to insert data
            cursor.execute('''
                INSERT INTO messages (name, email, phone, company, service, message)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, company, service, message))
            
            conn.commit() # Save changes
            conn.close()  # Connection close
            
            print("✅ Data Saved to Database Successfully!")
        except Exception as e:
            print(f"❌ Error saving to database: {e}")
        # -----------------------------------------------

        return redirect(url_for('home'))

    return render_template('contact.html')

@app.route('/projects')
def projects():
    return render_template('project.html')

# --- ADMIN ROUTE TO VIEW MESSAGES ---
@app.route('/view_messages')
def view_messages():
    # Database connect karke data layenge
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    data = cursor.fetchall()
    conn.close()

    # Ek simple si table bana ke browser pe dikha denge
    html_content = """
    <html>
    <head><title>Admin Panel</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h2>📬 Received Inquiries</h2>
        <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f2f2f2;">
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Company</th>
                <th>Service</th>
                <th>Message</th>
            </tr>
    """
    
    # Loop chala ke saare messages table me dalenge
    for row in data:
        html_content += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
                <td>{row[4]}</td>
                <td>{row[5]}</td>
                <td>{row[6]}</td>
            </tr>
        """
    
    html_content += "</table></body></html>"
    return html_content
# ------------------------------------
if __name__ == "__main__":
    init_db()  # App start hone se pehle Database initialize karega
    app.run(debug=True)