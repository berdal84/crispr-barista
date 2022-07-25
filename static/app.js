

const PENDING = -1
const SUCCESS = 0
const ERRROR = 1

class App {

    constructor(){
        console.log('App constructor()')
    }

    start(){
        console.log('App start()')
        this.update();
        this.check();
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

            this.setSpinner(true)
            const response = await (await result).json();
            this.setSpinner(false)
            
            if( response.code === SUCCESS )
            {
                if( response.payload.code === SUCCESS ) {
                    location.href = '/output'
                }
                else if ( response.payload.code === PENDING )
                {
                    alert('Running ...' );
                } else {
                    alert('An error occured! Check status bar.' );
                    location.reload()
                }
            }
            else
            {

            }
            
        });
    }

    setSpinner( visible ) {
        const el = document.getElementById("spinner");
        el.style.visibility = visible ? 'visible' : 'hidden';
    }

    async check() {

        this.setSpinner(true)

        const el       = document.getElementById("crispresso-check-status")
        el.innerText   = "checking";
        const raw      = await fetch('/check');
        const response = await raw.json();
        
        if( response.code == 0 ) {
            el.innerText = "DETECTED";
        } else {
            el.innerText = "NOT DETECTED. Did you installed it? Try to run CRISPResso -h from a terminal.";
        }

        this.setSpinner(false)
    }

    async update() {
        console.log('App update()')

        const raw    = await fetch('/status');
        const response = await raw.json();

        {
            const el = document.getElementById("status-msg");
            el.innerText = `Last message: ${response.payload.msg}`;
        }

        {
            const el = document.getElementById("status-cmd");
            el.innerText = `Last command: ${response.payload.cmd}`;
        }

        {
            const el = document.getElementById("status-code");
            el.innerText = `Last return code: ${response.payload.code}`;
        }

        setTimeout( () => this.update(), 1000 ); // loop back
    }
}

const app = new App();

document.addEventListener( 'DOMContentLoaded', (event) => { 
    app.start();
})
