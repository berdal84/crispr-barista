# CRISPResso UI

This is a simple UI to use localy CRISPResso from a web user interface.
The program uses Python3 and Flask.

## Prerequisites

[CRISPResso2](https://github.com/pinellolab/CRISPResso2) must be installed using [bioconda method](https://github.com/pinellolab/CRISPResso2#bioconda) (running `CRISPResso2 -h` must not fail).

Python3.7+ must be installed in a Unix-like operating system (MacOS or Linux).

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

## Captures

<p align="center">
  <img width="600" align="center" src="https://user-images.githubusercontent.com/942052/180898399-0bb94abc-8436-4cce-b7a4-8b7b1e9cb334.png"/>
</p>

