#!/bin/bash
deactivate
rm -r venv
virtualenv venv
source venv/bin/activate
pip install --upgrade -r requirements.txt