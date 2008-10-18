#
# $Id: Makefile,v 1.8 2008/10/18 00:56:14 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# Revision 1.8  2008/10/18 00:56:14  mjk
# copyright 5.1
#
# Revision 1.7  2008/03/06 23:41:57  mjk
# copyright storm on
#
# Revision 1.6  2007/06/23 04:04:00  mjk
# mars hill copyright
#
# Revision 1.5  2007/06/04 11:48:06  ssy
# Fix the way to patch globus_gram_job_manager_sge. More robust. No race condition.
#
# Revision 1.4  2007/06/04 10:41:55  ssy
# Fix wrong backup file name, causing trouble when build roll again from failed build
#
# Revision 1.3  2007/06/04 10:37:33  ssy
# Fix path to ROCKS arch command.
#
# Revision 1.2  2007/04/14 15:50:42  ssy
# Better support for globus-sge
# Prepare for ia64
#
# Revision 1.1  2007/04/03 14:34:40  ssy
# Add SGE WSGram support
# Old Pre-wsgram removed
# Not fully tested yet!
#

PKGROOT = /opt/globus
REDHAT.ROOT = $(PWD)/../../
ROCKSROOT = ../../../../..
ROCKSROOT.ABSOLUTE = $(shell cd $(ROCKSROOT); pwd)
# FIXME: Copied from $(ROCKSROOT)/etc/Rules.mk
ARCH.BIN = $(ROCKSROOT.ABSOLUTE)/bin/arch
ARCH = $(shell if [ ! -x ./_arch ]; then cp $(ARCH.BIN) _arch; fi; ./_arch)
-include $(ARCH).mk
#-include $(ROCKSROOT)/etc/Rules.mk
#include Rules.mk

#GLOBUS_FLAVOR=$(shell $(PKGROOT)/sbin/gpt-flavor-configuration  | egrep "^gcc.*:" | head -1 | sed "s/://g")
RPM_ARCH=$(shell uname -m | egrep -q "i.86" && echo i386 || uname -m)


GLOBUS_NOARCH_PKGS = globus_gram_job_manager_setup_sge-0.12 \
globus_wsrf_gram_service_java_setup_sge-1.1 \
globus_scheduler_event_generator_sge_setup-1.1

GLOBUS_ARCH_PKGS = globus_scheduler_event_generator_sge-1.1

globus_gram_job_manager_setup_sge-0.12 : globus_gram_job_manager_setup_sge-0.12.tar.gz 
	gzip -dc $^ | tar -xvf -
	(cd globus_gram_job_manager_setup_sge-0.12 && patch -p1 < ../sge-jobmanager.patch)

% : %.tar.gz
	gzip -dc $^ | tar -xvf -

.PHONY: rpm
rpm:: $(GLOBUS_NOARCH_PKGS) $(GLOBUS_ARCH_PKGS)
	# remove old package. FIXME: This destroy the SGE jobmanager installed on this machine!
	gpt-uninstall `gpt-query | grep -i _sge | awk '{print $1}'` || :
	for pkg in $(GLOBUS_NOARCH_PKGS); do \
		(gpt-build -srcdir $$pkg && \
		p=`echo $$pkg | sed "s/-[0-9.]\+$$//g"` && \
		gpt-pkg -native -pkgdir=$(PWD) -buildnumber=0 -rpmprefix=$(PKGROOT) $$p) \
	done 
	for pkg in $(GLOBUS_ARCH_PKGS); do \
		(gpt-build -srcdir $$pkg $(GLOBUS_FLAVOR) && \
		p=`echo $$pkg | sed "s/-[0-9.]\+$$//g"` && \
		gpt-pkg -native -pkgdir=$(PWD) -buildnumber=0 -rpmprefix=$(PKGROOT) $$p) \
	done 
	mkdir -p ../../RPMS/$(RPM_ARCH)
	cp -f *.rpm ../../RPMS/$(RPM_ARCH)

clean:: 
	rm -fr *.rpm
