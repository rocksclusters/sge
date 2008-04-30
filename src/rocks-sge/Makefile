#
# 
#

REDHAT.ROOT     = $(PWD)/../../
ROCKSROOT       = ../../../../..

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:
		
install::
	mkdir -p $(RPM_BUILD_ROOT)/etc/profile.d
	cp sge-binaries.* $(RPM_BUILD_ROOT)/etc/profile.d

	#mkdir -p $(RPM_BUILD_ROOT)/etc/rc.d/rocksconfig.d
	#cp post-* $(RPM_BUILD_ROOT)/etc/rc.d/rocksconfig.d

	mkdir -p $(RPM_BUILD_ROOT)/opt/gridengine/util/install_modules
	cp sge_configuration.conf \
		$(RPM_BUILD_ROOT)/opt/gridengine/util/install_modules

	mkdir -p $(RPM_BUILD_ROOT)/opt/gridengine/bin
	cp rocks-qlogin.sh $(RPM_BUILD_ROOT)/opt/gridengine/bin

	mkdir -p $(RPM_BUILD_ROOT)/opt/gridengine/mpi
	cp rocks-lam.template $(RPM_BUILD_ROOT)/opt/gridengine/mpi
	cp startlam.sh $(RPM_BUILD_ROOT)/opt/gridengine/mpi
	cp stoplam.sh $(RPM_BUILD_ROOT)/opt/gridengine/mpi

clean::
	rm -f $(NAME).spec.in

