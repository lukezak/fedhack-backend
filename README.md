# Hackathon : BioMedic backend

Simple python backend for fedhack ui (AKA BioMedic). Service provides facial biometric registration, matching and basic REST service data layer.

Basic flatfile comparison of `known` and `unknown` images are used to verify AuthN requires.


## Setup


### Dependencies

 - Python 2.7
 - pip
 - virtualenv
 - cmake

### Installation

Clone repo


    git clone https://github.com/lukezak/fedhack-backend.git

Setup virtual environment


    cd fedhack-backend
    virtualenv .venv
    . .venv/bin/activiate

Install dependencies

    pip install -r requirements.txt

Modify username and password for mongodb server in `settings.py`


## Run book

### Start

Run an instance of the backend service

   export PORT=5000 #exposes service on all IPs (without service will only be available on localhost)
   . .venv/bin/activiate
   nohup python run.py &

### Stop

   ^C



