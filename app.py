import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Database Link uthao
DATABASE_URL = os.environ.get('DATABASE_URL')

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

@app.route('/projects')
def projects():
    return render_template('project.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('tel')
        company = request.form.get('company')
        service = request.form.get('service')
        message = request.form.get('message')

        if DATABASE_URL:
            try:
                conn = psycopg2.connect(DATABASE_URL)
                cursor = conn.cursor()
                # Data Save kar rahe hain (Saare columns)
                cursor.execute('''
                    INSERT INTO messages (name, email, phone, company, service, message)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (name, email, phone, company, service, message))
                conn.commit()
                conn.close()
                print("✅ Data Saved!")
            except Exception as e:
                print(f"❌ Save Error: {e}")
        
        return redirect(url_for('home'))

    return render_template('contact.html')

# --- UPDATED ADMIN PANEL (Ab sab kuch dikhega) ---
@app.route('/view_messages')
def view_messages():
    if not DATABASE_URL:
        return "Database connect nahi hai!"
        
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages")
        data = cursor.fetchall()
        conn.close()

        # Table Headers (Ab 6 Columns hain)
        html = """
        <h2 style='font-family: sans-serif;'>📬 Inbox (Full Details)</h2>
        <table border='1' cellpadding='10' style='border-collapse: collapse; font-family: sans-serif; width: 100%;'>
            <tr style='background: #eee;'>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Company</th>
                <th>Service</th>
                <th>Message</th>
            </tr>
        """
        
        # Table Rows (Database se data nikal kar cell mein daalna)
        for row in data:
            html += f"""
            <tr>
                <td>{row[0]}</td> <td>{row[1]}</td> <td>{row[2]}</td> <td>{row[3]}</td> <td>{row[4]}</td> <td>{row[5]}</td> <td>{row[6]}</td> </tr>
            """
        
        html += "</table>"
        return html
    except Exception as e:
        return f"Error: {e}"

# --- ONE-TIME FIX ROUTE (Table Banane ke liye) ---
@app.route('/fix-db')
def fix_db():
    if not DATABASE_URL:
        return "Database URL nahi mili!"
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Table Create karo (Agar nahi hai toh)
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
        return "✅ Success! Database Table ban gayi hai. Ab /contact par jao."
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)