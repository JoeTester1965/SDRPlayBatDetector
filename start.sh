#!/bin/bash
nohup ./stop.sh 2>/dev/null
nohup python3 zmqpubsink.py  &> zmqpubsink.log &
nohup python3 SDRPlayBatDetector.py &> SDRPlayBatDetector.log  &
