#!/bin/bash 

SGE_ROOT=/opt/gridengine
SGE_CONFIG_FILE=$SGE_ROOT/util/install_modules/sge_configuration.conf

case $1 in
'-c')
	mkdir -p $SGE_ROOT/default/spool/qmaster
	chown -R sge:sge $SGE_ROOT
	(\
		cd $SGE_ROOT;	\
		./inst_sge -x -noremote	\
		-auto $SGE_CONFIG_FILE; \
	)
	cp $SGE_ROOT/default/common/sgeexecd /lib/svc/method/sgeexecd
	chmod a+x /lib/svc/method/sgeexecd
	rm -rf /etc/rc2.d/K02sgeexecd
	rm -rf /etc/rc2.d/S96sgeexecd
	rm -rf /etc/init.d/sgeexecd
	/lib/svc/method/sgeexecd stop
	;;

'-u')
	svcadm disable network/sge/execd
	rm -rf $SGE_ROOT/default/spool
	;;
esac
