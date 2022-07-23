from html import escape
from flask import render_template, url_for, Flask
from os import system

app = Flask(__name__)

@app.route("/")
def index():
    return render_template( "index.html", status=" ... " )

@app.route("/run")
def run():
    render_template( "index.html", status="Running ...")
    if( crispresso('-h') == 0):
        return render_template( "index.html", status="CRISPResso is done")
    return index()

@app.route("/check")
def check():
    if( crispresso('-h') == 0):
        return render_template( "index.html", status="CRISPResso is working!")
    return index()

def crispresso( args ):
    return system(f'CRISPResso {args}')