# CRISPResso UI

This is a simple UI to use localy CRISPResso from a web user interface.
The program uses Python3 and Flask.

## Prerequisites

CRISPResso2 must be installed using [bioconda method](https://github.com/pinellolab/CRISPResso2#bioconda) (running `CRISPResso2 -h` must not fail).

Python3 must be installed in a Unix-like operating system (MacOS or Linux).

## Usage

### `./install.sh`

Initialize a local environment and install dependencies.
Python3 is required.

### `./run.sh`

Launches the application.
Once you see `* Running on http://127.0.0.1:5000 (Press CTRL+C to quit)` open `http://127.0.0.1:5000` with your favorite browser.

*Warning: do not deploy in production, use only localy*

### `./dev.sh`

Launches the application in debug mode.
