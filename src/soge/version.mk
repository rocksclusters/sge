PKGROOT		= /opt/gridengine
NAME		= sge
VERSION		= 8.1.9
RELEASE		= 1
ifeq ($(strip $(VERSION.MAJOR)), 5)
PATCHDIR        = patch-files-5
else
PATCHDIR        = patch-files
endif 
RPM.FILES	= $(PKGROOT)
