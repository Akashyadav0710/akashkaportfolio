from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/projects')
def projects():
    return render_template('project.html')

if __name__ == "__main__":
    app.run(debug=True)