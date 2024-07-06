#!/bin/bash
nohup pkill -f zmqpubsink.py  &> /dev/null
nohup pkill -f SDRPlayBatDetector.py  &> /dev/null
nohup pkill -9 -f zmqpubsink.py  &> /dev/null
nohup pkill -9 -f SDRPlayBatDetector.py  &> /dev/null