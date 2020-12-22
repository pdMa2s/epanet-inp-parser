#!/bin/bash         
python epanet_inp_parser.py 
export FLASK_APP=wd.py
export FLASK_ENV=development
export FLASK_DEBUG=0
python -m flask run 
