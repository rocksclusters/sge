NAME		= rocks-sge
#VERSION		= V60u6
RELEASE		= 2
PKGROOT = /opt/gridengine
RPM.FILES = \
/etc/profile.d/* \n\
$(PKGROOT)/util/install_modules/* \n \
$(PKGROOT)/bin/* \n \
$(PKGROOT)/mpi/* 
