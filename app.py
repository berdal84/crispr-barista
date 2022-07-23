from html import escape
from flask import render_template, url_for, Flask
from os import system

app = Flask(__name__)

@app.route("/")
def index( status = " ... "):
    return render_template( "index.html", status=f"{status}" )

@app.route("/form")
def form():
    return render_template( "form.html" )

@app.route("/run")
def run():
    render_template( "index.html", status="Running ...")
    if( crispresso('-h') == 0):
        return index("CRISPResso is done")
    return index()

@app.route("/check")
def check():
    if( crispresso('-h') == 0):
        return index("CRISPResso is working!")
    return index()

def crispresso( args ):
    return system(f'CRISPResso {args}')