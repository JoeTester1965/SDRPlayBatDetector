#!/bin/bash
nohup ./stop.sh 2>/dev/null
nohup python3 zmqpubsink.py 2>/dev/null &
nohup python3 SDRPlayBatDetector.py 2>/dev/null &