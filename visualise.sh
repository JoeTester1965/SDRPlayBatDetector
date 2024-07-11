#!/bin/bash

VIRTUAL_ENV=$PWD/venv/bin/activate

#Use a python virtual env if needed
if [ -s $VIRTUAL_ENV_IF_NEEDED ]; then
	source $VIRTUAL_ENV
else
    echo "No local python virtual env at $VIRTUAL_ENV is being used "
fi

python3 ./csv_viewer.py

exit