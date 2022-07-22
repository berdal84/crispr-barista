from html import escape
from flask import url_for, Flask

app = Flask(__name__)

@app.route("/")
@app.route('/run/<command>')
def home(command = 'none'):
    url_for('static', filename='static/style.css')
    return f"""
        <html>
        <head>
            <link rel="stylesheet" href="/static/style.css"/>
        </head>
        <body>
        <div class="container">
            <h1>Hello, World!</h1>
            <p>This is the upcoming CRISPResso UI.</p>
            <a href="/run/analysis">Run analysis</a>
            <p>Current command: { escape(command)}</p>
        </div>
        </body>
        </html>
        """
