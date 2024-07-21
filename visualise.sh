#!/bin/bash

VIRTUAL_ENV=$PWD/venv/bin/activate

#Use a python virtual env if needed
if [ -s $VIRTUAL_ENV_IF_NEEDED ]; then
	source $VIRTUAL_ENV
else
    echo "No local python virtual env at $VIRTUAL_ENV is being used "
fi

python3 ./csv_viewer.py

if [[ -z $1 ]]
then
	dir=./output/$(date +%d-%m-%Y-%H-%M)
else
	dir=$1/$(date +%d-%m-%Y-%H-%M)
fi

mkdir -p $dir

cp -f events-by-frequency.jpg events-by-timeofday.jpg $dir

exit