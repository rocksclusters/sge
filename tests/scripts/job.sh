#!/bin/bash
#
#$ -S /bin/bash
#$ -cwd
#$ -o output.log
#$ -o error.log


echo running on `hostname`
sleep 5
touch testsge
echo done running on `hostname`

