from flask import render_template, Flask, flash, request
from os import system, path

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Required by flash
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024    # 2 Gb limit

FASTQ_R1_PATH  = "./uploads/fastq_r1.fastq"
FASTQ_R2_PATH  = "./uploads/fastq_r2.fastq"
OUTPUT_FOLDER  = "./output"

@app.route("/")
def index(status=" ... "):
    return render_template("index.html", status=f"{status}")


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/run", methods =["GET", "POST"])
def run():
    flash('Running CRISPResso -h command ...')

    if request.method == "POST":

        fastq_r1 = request.files['fastq_r1']
        fastq_r2 = request.files['fastq_r2']

        amplicon_seq    = request.form.get("amplicon_seq")
        guide_seq       = request.form.get("guide_seq")

        args = ''

        if not fastq_r1:                                # fastq_r1
            flash('No fastq_r1 file', 'error')
        else:
            fastq_r1.save(FASTQ_R1_PATH)
            args += f' --fastq_r1 {FASTQ_R1_PATH}'

        if not fastq_r2:                                # fastq_r2
            flash('No fastq_r2 file', 'error')
        else:
            fastq_r2.save(FASTQ_R2_PATH)
            args += f' --fastq_r2 {FASTQ_R2_PATH}'

        if not amplicon_seq:                            # amplicon_seq
            flash('No amplicon_seq file', 'error')
        else:
            args += f' --amplicon_seq {amplicon_seq}'

        if not guide_seq:                               # guide_seq
            flash('No guide_seq file', 'error')
        else:
            args += f' --guide_seq {guide_seq}'

        args += f" --output_folder {OUTPUT_FOLDER}"

        if fastq_r1 and fastq_r2 and amplicon_seq and guide_seq and crispresso(args) == 0 :
            return index("Finished!")
        return index("Unable to run!")
    else:
        return index("Require to POST data.")

@app.route("/check")
def check():
    if(crispresso('-h') == 0):
        return index("CRISPResso is working!")
    return index()


def crispresso(args ):
    command = f'CRISPResso {args}'
    flash(f"Running {command}")
    return system( command )
