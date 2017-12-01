# $Id: Makefile,v 1.8 2012/11/27 00:49:31 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.8  2012/11/27 00:49:31  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.7  2012/05/06 05:49:43  phil
# Copyright Storm for Mamba
#
# Revision 1.6  2011/07/23 02:31:36  phil
# Viper Copyright
#
# Revision 1.5  2010/09/07 23:53:25  bruno
# star power for gb
#
# Revision 1.4  2009/05/01 19:07:22  mjk
# chimi con queso
#
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
