#!/bin/bash
nohup pkill -f zmqpubsink.py  &> /dev/null
nohup pkill -f SDRPlayBatDetector.py  &> /dev/null