#!/usr/bin/bash

# This files trains the g2p models iteratively. The g2p.py file is downloaded
# from this link http://www-i6.informatik.rwth-aachen.de/web/Software/g2p.html


export PYTHONPATH=/l/SRC/g2p/lib/python2.7/site-packages

## TRAIN G2P MODEL ##
/l/SRC/g2p/bin/g2p.py --train train.lex --devel 5% --write-model model-1

/l/SRC/g2p/bin/g2p.py --model model-1 --ramp-up --train train.lex --devel 5% --write-model model-2

/l/SRC/g2p/bin/g2p.py --model model-2 --ramp-up --train train.lex --devel 5% --write-model model-3

/l/SRC/g2p/bin/g2p.py --model model-3 --ramp-up --train train.lex --devel 5% --write-model model-4

/l/SRC/g2p/bin/g2p.py --model model-4 --ramp-up --train train.lex --devel 5% --write-model model-5

/l/SRC/g2p/bin/g2p.py --model model-5 --ramp-up --train train.lex --devel 5% --write-model model-6

## TEST G2P MODEL ##
/l/SRC/g2p/bin/g2p.py --model model-6 --test test.lex
