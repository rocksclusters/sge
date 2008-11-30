#
# 
#

REDHAT.ROOT     = $(CURDIR)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
		
install::
	mkdir -p $(ROOT)/etc/profile.d
	cp sge-binaries.* $(ROOT)/etc/profile.d
	mkdir -p $(ROOT)/opt/gridengine/util/install_modules
	cp sge_configuration.conf \
		$(ROOT)/opt/gridengine/util/install_modules
	mkdir -p $(ROOT)/opt/gridengine/bin
	cp rocks-qlogin.sh $(ROOT)/opt/gridengine/bin
	mkdir -p $(ROOT)/opt/gridengine/mpi
	cp rocks-lam.template $(ROOT)/opt/gridengine/mpi
	cp startlam.sh $(ROOT)/opt/gridengine/mpi
	cp stoplam.sh $(ROOT)/opt/gridengine/mpi

clean::
