import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Render se Database ka Link uthayenge
DATABASE_URL = os.environ.get('DATABASE_URL')

# --- DATABASE SETUP FUNCTION ---
def init_db():
    # Agar Database Link nahi mila (matlab Localhost), toh kuch mat karo
    if not DATABASE_URL:
        return

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        # Table Create (Postgres Syntax)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
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
        print("✅ Database Connected & Table Ready!")
    except Exception as e:
        print(f"❌ DB Error: {e}")
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
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('tel')
        company = request.form.get('company')
        service = request.form.get('service')
        message = request.form.get('message')

        # Agar Database connected hai, tabhi save karo
        if DATABASE_URL:
            try:
                conn = psycopg2.connect(DATABASE_URL)
                cursor = conn.cursor()
                # Postgres me '?' ki jagah '%s' use hota hai
                cursor.execute('''
                    INSERT INTO messages (name, email, phone, company, service, message)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (name, email, phone, company, service, message))
                
                conn.commit()
                conn.close()
                print("✅ Data Saved to Cloud!")
            except Exception as e:
                print(f"❌ Save Error: {e}")
        
        return redirect(url_for('home'))

    return render_template('contact.html')

@app.route('/projects')
def projects():
    return render_template('project.html')

# --- ADMIN PANEL (Messages Dekhne ke liye) ---
@app.route('/view_messages')
def view_messages():
    if not DATABASE_URL:
        return "<h3>Database not connected (Check Environment Variable)</h3>"
        
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages")
        data = cursor.fetchall()
        conn.close()

        html = """
        <h2 style='font-family: sans-serif;'>📬 Inbox (Cloud DB)</h2>
        <table border='1' cellpadding='10' style='border-collapse: collapse; font-family: sans-serif;'>
            <tr style='background: #eee;'><th>Name</th><th>Email</th><th>Message</th></tr>
        """
        for row in data:
            html += f"<tr><td>{row[1]}</td><td>{row[2]}</td><td>{row[6]}</td></tr>"
        
        html += "</table>"
        return html
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)