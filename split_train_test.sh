#!/usr/bin/bash

# Take 9 lines in every 10 as train and remaining one as test
total_data=$1
awk 'NR % 10 != 0' $total_data > train.lex
awk 'NR % 10 == 0' $total_data > test.lex

