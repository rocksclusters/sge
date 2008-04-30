#/bin/sh
#
#$ -cwd
#$ -j y
#$ -S /bin/sh

MPI_HOME=/opt/mpich/gnu
$MPI_HOME/bin/mpirun -np $NSLOTS -machinefile $TMPDIR/machines cpi
