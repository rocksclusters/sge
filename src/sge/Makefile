#
# $Id: Makefile,v 1.33 2008/04/22 23:07:22 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
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
# Revision 1.33  2008/04/22 23:07:22  bruno
# qlogin and qrsh now works with latest SGE
#
# Revision 1.32  2008/03/06 23:41:58  mjk
# copyright storm on
#
# Revision 1.31  2008/02/29 18:38:45  bruno
# refresh SGE
#
# Revision 1.30  2007/06/23 04:04:01  mjk
# mars hill copyright
#
# Revision 1.29  2007/05/25 20:55:47  bruno
# first pass at version 6.1
#
# Revision 1.28  2007/04/10 10:24:41  ssy
# Change openssl installation path
#
# Revision 1.27  2007/04/03 14:34:40  ssy
# Add SGE WSGram support
# Old Pre-wsgram removed
# Not fully tested yet!
#
# Revision 1.26  2007/01/09 01:27:16  mjk
# missing file for sge gram
#
# Revision 1.25  2006/09/11 22:50:17  mjk
# monkey face copyright
#
# Revision 1.24  2006/08/10 00:12:00  mjk
# 4.2 copyright
#
# Revision 1.23  2006/08/09 18:44:23  mjk
# fix target for sge.pm
#
# Revision 1.22  2006/08/08 01:39:22  mjk
# i think this is everything the GRAM needs now
#
# Revision 1.21  2006/08/08 00:59:18  mjk
# tweak file location (more to come)
#
# Revision 1.20  2006/08/02 22:23:37  mjk
# added GRAM to SGE rpm
#
# Revision 1.19  2006/06/26 20:11:03  bruno
# added patch to do better cleanup on MPI programs that are launched from
# SGE. that is, qdel will correctly cleanup all the processes
#
# Revision 1.18  2006/06/26 19:05:37  bruno
# refreshed to version 6 update 8
#
# Revision 1.17  2005/12/30 18:28:08  mjk
# remove all spec files
#
# Revision 1.16  2005/10/12 18:10:56  mjk
# final copyright for 4.1
#
# Revision 1.15  2005/09/16 01:04:34  mjk
# updated copyright
#
# Revision 1.14  2005/09/15 18:15:25  bruno
# i386 sge v6 updates
#
# Revision 1.13  2005/08/25 17:53:34  bruno
# cleanup
#
#

PKGROOT		= /opt/gridengine
REDHAT.ROOT     = $(PWD)/../../
ROCKSROOT       = ../../../../..

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

DISTPATH=`rocks-dist --path=dist.getRPMSPath paths`


build:	prep patch
	( cd gridengine/source ; \
		cp ../../aimk.private . ; \
		cp ../../build.properties . ; \
		./aimk -only-depend ; \
		scripts/zerodepend ; \
		./aimk depend ; \
		./aimk ;\
		./aimk -man ; \
	)

prep:
	tar zvfx ge-$(VERSION)_TAG-src.tar.gz

	rocks-dist --notorrent dist
	mkdir -p $(PWD)/gridengine/source/$(SGE_ARCH)/var/lib/rpm
	rpm -ivh --root=$(PWD)/gridengine/source/$(SGE_ARCH) \
		--nodeps --noscripts \
		$(DISTPATH)/db4*.$(ARCH).rpm
	mkdir -p $(PWD)/gridengine/source/var/lib/rpm
	rpm -ivh --root=$(PWD)/gridengine/source/ \
		--nodeps --noscripts \
		$(DISTPATH)/openssl-devel*.$(ARCH).rpm
	-ln -s $(PWD)/gridengine/source/usr/$(LIBARCH) \
		$(PWD)/gridengine/source/usr/lib

patch:
	( cd patch-files/$(VERSION) ; \
		find . -type f | grep -v CVS | cpio -pduv ../.. ; \
	)

install::
	( cd gridengine/source ; \
		mkdir -p $(RPM_BUILD_ROOT)/$(PKGROOT) ; \
		cp ../../distinst.private . ; \
		ln -s usr/bin $(SGE_ARCH)/bin ; \
		echo Y | SGE_ROOT=$(RPM_BUILD_ROOT)/$(PKGROOT) \
			scripts/distinst -local -noexit -allall $(SGE_ARCH) ; \
	)

clean::
	rm -rf gridengine
	rm -rf rocks-dist cachedir

