from html import escape
from flask import url_for, Flask
from os import system

app = Flask(__name__)

@app.route("/")
@app.route('/crispresso')
@app.route('/crispresso/<command>')
def home(command = 'none'):

    if( command != 'none' ):
        crispresso('-h')

    url_for('static', filename='static/style.css')
    return f"""
        <html>
        <head>
            <title>CRISPResso UI</title>
            <link rel="stylesheet" href="/static/style.css"/>
        </head>
        <body>
        <div class="container">
            <h1>Hello, World!</h1>
            <p>This is the upcoming CRISPResso UI.</p>
            <p>Current command: { escape(command)}</p>

            <a href="/crispresso/help">Get help</a>
            <a href="/crispresso">Run</a>
        </div>
        </body>
        </html>
        """

def crispresso( args ):
    system(f'CRISPResso ${args}')