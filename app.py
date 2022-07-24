from flask import render_template, Flask, flash, request, redirect, json
from multiprocessing import Pool
from os import system
from dataclasses import dataclass

@dataclass
class Status:
    cmd: str  = " ... "
    msg: str  = " ... "
    code: str = " ... "

app = Flask(__name__)
pool = Pool(processes=1) # Start a worker processes.

status = Status()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Required by flash
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024    # 2 Gb limit

FASTQ_R1_PATH  = "./uploads/fastq_r1.fastq"
FASTQ_R2_PATH  = "./uploads/fastq_r2.fastq"
OUTPUT_FOLDER  = "./static/output"

@app.route("/")
def getIndex(message=""):
    if message:
        status.msg = message
    return render_template("index.html", status=status)

@app.route("/status")
def getStatus():
    return json.jsonify( status )

@app.route("/form")
def getForm():
    return render_template("form.html")

@app.route("/output/")
def getOutput():
    return render_template("iframe.html", iframe_src="/static/output/CRISPResso_on_fastq_r1_fastq_r2.html")
    

@app.route("/run", methods =["GET", "POST"])
def run():

    if request.method == "POST":

        flash('Preparing arguments for CRISPResso ...')

        status.code = ' ... '

        fastq_r1 = request.files['fastq_r1']
        fastq_r2 = request.files['fastq_r2']

        amplicon_seq    = request.form.get("amplicon_seq")
        guide_seq       = request.form.get("guide_seq")

        args = ''

        if not fastq_r1:                                # fastq_r1
            flash('No fastq_r1 file')
        else:
            fastq_r1.save(FASTQ_R1_PATH)
            args += f' --fastq_r1 {FASTQ_R1_PATH}'

        if not fastq_r2:                                # fastq_r2
            flash('No fastq_r2 file')
        else:
            fastq_r2.save(FASTQ_R2_PATH)
            args += f' --fastq_r2 {FASTQ_R2_PATH}'

        if not amplicon_seq:                            # amplicon_seq
            flash('No amplicon_seq file')
        else:
            args += f' --amplicon_seq {amplicon_seq}'

        if not guide_seq:                               # guide_seq
            flash('No guide_seq file')
        else:
            args += f' --guide_seq {guide_seq}'

        args += f" --output_folder {OUTPUT_FOLDER}"

        if fastq_r1 and fastq_r2 and amplicon_seq and guide_seq:
            flash('Running CRISPResso with arguments ...')
            crispressoAsync(args)
        else:
            flash('Unable to prepare arguments for CRISPResso!')

        return getStatus()
    else:
        return getIndex("Require to POST data.")

@app.route("/check")
def check():
    status.msg = 'Checking CRISPResso ...'
    crispressoAsync('-h')
    return getStatus()

def crispresso(args ):
    command = f'CRISPResso {args}'
    status.msg = 'Running command ...'
    status.code = ' ... '
    status.cmd = command
    status.code = system( command )

def crispressoAsync( args ):
    command = f'CRISPResso {args}'
    status.msg = 'Running command ...'
    status.cmd = command
    status.code = -1
    result = pool.apply_async(system, [command], callback=onCrispressoFinished ) # Evaluate "f(10)" asynchronously calling callback when finished.
    return getStatus();

def onCrispressoFinished( returnCode ):
    status.code = returnCode
    if( returnCode == 0 ):
        status.msg = 'Command return SUCCESS'
    else:
        status.msg = 'Command return ERROR'
