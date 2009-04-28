# $Id: Makefile,v 1.3 2009/04/22 01:36:39 anoop Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.3  2009/04/22 01:36:39  anoop
# Minor mod
#
# Revision 1.2  2009/04/22 01:30:41  anoop
# Upgraded SGE for Solaris to match Linux version
#
# Revision 1.1  2008/11/30 19:32:49  anoop
# Added support for SGE on Solaris
#
#

PKGROOT	= /opt/gridengine
REDHAT.ROOT = $(CURDIR)/../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:

install::
	mkdir -p $(ROOT)/$(PKGROOT)
	gunzip -c $(NAME)-$(VERSION)$(RELEASE)-bin-sol-amd64.tar.gz \
		| (cd $(ROOT)/$(PKGROOT); $(TAR) -xf -)
	gunzip -c $(NAME)-$(VERSION)$(RELEASE)-bin-sol-x86.tar.gz \
		| (cd $(ROOT)/$(PKGROOT); $(TAR) -xf -)
	gunzip -c $(NAME)-$(VERSION)$(RELEASE)-common.tar.gz \
		| (cd $(ROOT)/$(PKGROOT); $(TAR) -xf -)
	(cd patch-files/$(VERSION)$(RELEASE) && find . -type f | grep -v CVS | cpio -pudv $(ROOT)/$(PKGROOT))
	mkdir -p $(ROOT)/$(INIT_SCRIPTS_DIR)
	mkdir -p $(ROOT)/$(PKGROOT)/share/
	$(INSTALL) -m0755 sge_exec_setup.sh $(ROOT)/$(PKGROOT)/share/
	$(INSTALL) -m0644 sge_exec.xml $(ROOT)/$(PKGROOT)/share/
	
clean::