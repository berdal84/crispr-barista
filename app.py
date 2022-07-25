from ast import Str
from json import dump
from sys import path
path.insert(0, 'src/fastq.py')

from sre_constants import SUCCESS
from flask import jsonify, render_template, Flask, flash, request, redirect, json
from multiprocessing import Pool
import os
from dataclasses import dataclass
from src.fastq import Fastq

SUCCESS = 0
ERROR   = 1
PENDING = -1

@dataclass
class Status:
    cmd: str  = " ... "
    msg: str  = " ... "
    code: int = PENDING
    checked: bool = False

@dataclass
class Response:
    code: int
    msg: str
    payload: any

app = Flask(__name__)
pool = Pool(processes=1) # Start a worker processes.

status = Status()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Required by flash
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024    # 2 Gb limit

FASTQ_TO_SPLIT_PATH = "./uploads/fastq_to_split.fastq"
FASTQ_R1_PATH  = "./uploads/fastq_r1.fastq"
FASTQ_R2_PATH  = "./uploads/fastq_r2.fastq"
N_PROCESSES    = 'max'

@app.route("/")
def getIndex(message=""):
    if message:
        status.msg = message
    return render_template("index.html", status=status)

@app.route("/status")
def getStatus():
    return success( "Status returned", status)

@app.route("/output/")
def getOutput():
    return render_template("iframe.html", iframe_src=f"/static/output/CRISPResso_on_output.html")
    
def error( msg: str = 'Error', payload: object = {}):
    return json.jsonify( Response( ERROR, msg, payload ) )

def success( msg: str = 'Success', payload: object = {}):
    return json.jsonify( Response( SUCCESS, msg, payload ) )

@app.route("/run", methods =["GET", "POST"])
def run():

    if request.method == "POST":

        status.msg = 'Preparing arguments for CRISPResso ...'
        status.cmd = 'run()'
        status.code = PENDING

        # clear old files

        status.msg = "Cleaning existing files ..."
        if os.path.exists(FASTQ_R1_PATH):
            os.remove(FASTQ_R1_PATH)
        if os.path.exists(FASTQ_R2_PATH):
            os.remove(FASTQ_R2_PATH)
        if os.path.exists(FASTQ_TO_SPLIT_PATH):
            os.remove(FASTQ_TO_SPLIT_PATH)

        # get form/files from request
        status.msg = "Getting request form values and files ..."
        split_on        = request.form.get('split', False)
        fastq_r1        = request.files.get('fastq_r1')
        fastq_r2        = request.files.get('fastq_r2')
        amplicon_seq    = request.form.get("amplicon_seq")
        guide_seq       = request.form.get("guide_seq")
        
        # prepare files
        if not split_on:
            fastq_r1.save(FASTQ_R1_PATH)
            fastq_r2.save(FASTQ_R2_PATH)
        else:
            status.msg = 'Splitting ...'
            fastq_r1.save(FASTQ_TO_SPLIT_PATH)

            if not Fastq.split_r1r2( FASTQ_TO_SPLIT_PATH, FASTQ_R1_PATH, FASTQ_R2_PATH ):
                return error("Unable to split %s" %FASTQ_TO_SPLIT_PATH)
            status.msg = 'Splitting OK, try to open files ...'
            fastq_r1 = open(FASTQ_R1_PATH)
            fastq_r2 = open(FASTQ_R2_PATH)


        # build argument string
        status.msg = 'Making command line arguments ...'

        args = ''

        args += f' --fastq_r1 {FASTQ_R1_PATH}'
        args += f' --fastq_r2 {FASTQ_R2_PATH}'
        args += f' --amplicon_seq {amplicon_seq}'
        args += f' --guide_seq {guide_seq}'
        args += f" --output_folder ./static/output"
        args += f" --n_processes {N_PROCESSES}"
        args += f" --name output"

        # 2 - analysis
        status.msg = 'Check and run CRISPResso ...'

        if not fastq_r1:
            return error('Unable to open the fastq R1!', status)

        if not fastq_r2:
            return error('Unable to open the fastq R2!', status)
            
        if not amplicon_seq:
            return error('No amplicon sequence specified!', status)

        if not guide_seq:
            return error('No amplicon sequence specified!', status)

        code = crispresso(args)
        if code == SUCCESS :
                return success( 'Command finished ...', status)
        elif code == PENDING :
                return success( 'Command pending ...', status)
        return error('CRISPResso command failed!', status)
        
    else:
        return error('/run require POST method!', status)

@app.route("/check")
def check():
    if status.checked:
        return success("Already checked")
    if crispresso("-h") == SUCCESS:
        status.checked = True
        return success("First check")
    return error()

def crispresso(args, asyncronously=False ):
    command     = f'CRISPResso {args}'
    msg         = 'Running command ...'
    status.msg  = msg
    status.cmd  = command # FixMe: before to put in production ! Clean command
    status.code = PENDING
    if asyncronously:
        pool.apply_async(os.system, [command], callback=onCrispressoFinished ) # Evaluate "f(10)" asynchronously calling callback when finished.
    else:
        status.code = os.system( command )
    return status.code

def onCrispressoFinished( returnCode ):
    status.code = returnCode
    if( returnCode == SUCCESS ):
        status.msg = 'Command return SUCCESS'
    else:
        status.msg = 'Command return ERROR'
