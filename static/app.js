

const ReturnCode = Object.freeze({
    PENDING: -1,
    SUCCESS: 0,
    ERRROR: 1,
    toString: ( code ) => {
        switch( code )
        {
            case -1: return "PENDING"
            case 0: return  "SUCCESS"
            default: return "ERROR"
        }
    }
})

class App {

    constructor(){
        console.log('App constructor()')
    }

    start(){
        console.log('App start()')
        this.update();
        this.check();

        const splitCheckbox  = document.getElementById('split')
        const fastqR2Fs      = document.getElementById('fastq-r2-fs')
        const fastqR2SplitOn = document.getElementById('fastq-r2-split-on')
        
        splitCheckbox?.addEventListener('change', (event) => {
            const splitOn = event.currentTarget.checked
            fastqR2Fs.disabled        = splitOn
            fastqR2SplitOn.hidden     = !splitOn
        })

        document.addEventListener('submit', async (e) => {
            // Store reference to form to make later code easier to read
            const form = e.target;
        
            // Post data using the Fetch API
            const result = fetch(form.action, {
                method: form.method,
                body: new FormData(form),
            });
        
            // Prevent the default form submit
            e.preventDefault();

            this.showLoadingOverlay(true)
        
            try {
                const response = await (await result).json();

                switch( response.code )
                {                    
                    case ReturnCode.SUCCESS:
                        switch( response.payload.code )
                        {
                            case ReturnCode.SUCCESS:
                                location.href = '/output'
                                break;
                            
                            case ReturnCode.ERROR:
                                alert( `Error in CRISPResso command!` );
                                break;

                            case ReturnCode.PENDING:
                                alert( `CRISPResso command pending ...`  );
                        }
                        break;

                    case ReturnCode.ERRROR:
                        alert( `Error: ${response.msg}` );
                        break;
                    
                    case ReturnCode.PENDING:
                        alert( `Pending ... : ${response.msg}` );
                }
            } 
            catch( e ) {
                alert('Server internal error!' );
            }

            this.showLoadingOverlay(false)
            
        });
    }

    showLoadingOverlay( visible ) {
        const el = document.getElementById("spinner");
        el.style.visibility = visible ? 'visible' : 'hidden';
    }

    async check() {

        this.showLoadingOverlay(true)

        const el       = document.getElementById("crispresso-check-status")
        el.innerText   = "checking";
        const raw      = await fetch('/check');
        const response = await raw.json();
        
        if( response.code == ReturnCode.SUCCESS ) {
            el.innerText = "DETECTED";
        } else {
            el.innerText = "NOT DETECTED. Did you installed it?";
        }

        this.showLoadingOverlay(false)
    }

    async update() {
        console.log('App update()')

        const raw      = await fetch('/status');
        const response = await raw.json();

        {
            const el = document.getElementById("status-msg");
            const txt = `message: ${response.payload.msg}`;
            if( el.innerText !== txt )
                el.innerText = txt
        }

        {
            const el = document.getElementById("spinner-msg");
            const txt = response.payload.msg;
            if( el.innerText !== txt )
                el.innerText = txt
        }

        {
            const el = document.getElementById("status-cmd");
            const txt = `command: ${response.payload.cmd}`;
            if( el.innerText !== txt )
                el.innerText = txt
        }

        {
            const el = document.getElementById("status-code");
            const txt = `code: ${ReturnCode.toString(response.payload.code)} (${response.payload.code})`;
            if( el.innerText !== txt )
                el.innerText = txt
        }

        setTimeout( () => this.update(), 500 ); // loop back
    }
}

const app = new App();

document.addEventListener( 'DOMContentLoaded', () => { app.start(); })
