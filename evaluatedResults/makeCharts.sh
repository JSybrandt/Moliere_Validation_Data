#!/bin/bash

./makePublishedVsNoise.py &
./makeHighlyCitedVsNoise.py &

wait

scp published_roc.png severn:~/Downloads/
scp highly_cited_roc.png severn:~/Downloads/
