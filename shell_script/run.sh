#!/bin/bash
echo "SimCmp N=15 a=4"
python shor.py -s local --simcmp --nor 15 4
echo "SimCmp N=21 a=8"
python shor.py -s local --simcmp --nor 21 8
echo "SimCmp N=33 a=10"
python shor.py -s local --simcmp --nor 33 10
echo "SimCmp N=35 a=6"
python shor.py -s local --simcmp --nor 35 6
echo "SimCmp N=39 a=14"   
python shor.py -s local --simcmp --nor 39 14