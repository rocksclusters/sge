#!/bin/bash
#
# Test SGE
#
# maxrun time 2 minutes

function reportError {
	echo $1
	exit -1
}


function Pause {
	echo $1 press any key to continue execution
	OLDCONFIG=`stty -g`
	stty -icanon -echo min 1 time 0
	dd count=1 2>/dev/null
	stty $OLDCONFIG
}


TESTUSER=testsge

echo creating user test
useradd -m $TESTUSER
rocks sync users

while [ true ]; do
	sleep 5
	if [ -d /home/$TESTUSER/ ];then
		break
	fi
done

echo submitting jog to sge
cp -p scripts/job.sh /home/$TESTUSER/
chown $TESTUSER /home/$TESTUSER/job.sh
su - $TESTUSER -c "qsub -sync y job.sh " || reportError "Unable to run condor_submit"

if [ ! -f /home/$TESTUSER/testsge ];then
	reportError "Condor job did not create the test file."
else
        echo Sucesfully tested sge submission
        exit
fi

 
