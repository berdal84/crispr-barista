

class App {

    constructor(){
        console.log('App constructor()')
    }

    start(){
        console.log('App start()')
        this.update();

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

            const json = await (await result).json();
            if( json.code === 0 ) {
                location.href = '/output'
            } else {
                alert('An error occured! Check status bar.' );
                location.reload()
            }
        });
    }

    async check() {
        const raw    = await fetch('/check');
        const result = await raw.json();
        console.log(result);
    }

    async update() {
        console.log('App update()')

        const raw    = await fetch('/status');
        const status = await raw.json();

        {
            const el = document.getElementById("status-msg");
            el.innerText = `Last message: ${status.msg}`;
        }

        {
            const el = document.getElementById("status-cmd");
            el.innerText = `Last command: ${status.cmd}`;
        }

        {
            const el = document.getElementById("status-code");
            el.innerText = `Last return code: ${status.code}`;
        }

        setTimeout( () => this.update(), 1000 ); // loop back
    }
}

const app = new App();

document.addEventListener( 'DOMContentLoaded', (event) => { 
    app.start();
})
