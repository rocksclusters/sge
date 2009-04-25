# 
# $Id: Makefile,v 1.24 2009/04/25 03:56:02 bruno Exp $
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
# Revision 1.24  2009/04/25 03:56:02  bruno
# tweaks
#
# Revision 1.23  2008/11/05 17:24:22  bruno
# fix to build usersguide
#
# Revision 1.22  2008/10/18 00:56:14  mjk
# copyright 5.1
#
# Revision 1.21  2008/03/06 23:41:58  mjk
# copyright storm on
#
# Revision 1.20  2007/06/23 04:04:01  mjk
# mars hill copyright
#
# Revision 1.19  2006/09/15 01:42:11  mjk
# *** empty log message ***
#
# Revision 1.18  2006/09/11 22:50:17  mjk
# monkey face copyright
#
# Revision 1.17  2006/08/10 00:12:00  mjk
# 4.2 copyright
#
# Revision 1.16  2005/12/30 18:28:09  mjk
# remove all spec files
#
# Revision 1.15  2005/10/18 20:20:37  bruno
# automatically set the copyright date
#
# Revision 1.14  2005/10/12 18:10:56  mjk
# final copyright for 4.1
#
# Revision 1.13  2005/09/16 01:04:34  mjk
# updated copyright
#
# Revision 1.12  2005/08/24 23:34:51  bruno
# update to sge6
#
# Revision 1.4  2005/05/24 21:23:53  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/04/05 22:21:47  nadya
# move logic of creating rocks.dsl, rocks.css and stylesheet-images to Rules.mk
# Add target predoc in order to make docs in a local directory
#
# Revision 1.2  2005/03/29 05:07:06  tsailm
# Cleanup for cvs log tag
#



PKGROOT		= /var/www/html/roll-documentation/sge/$(VERSION)
REDHAT.ROOT	= $(PWD)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

default: $(NAME).spec ../$(NAME)-$(VERSION).tar.gz

html: predoc
	jw --backend html --dsl $(PWD)/rocks.dsl#html index.sgml 

pdf: predoc
	jw --backend pdf --dsl $(PWD)/rocks.dsl#print index.sgml

build: html pdf

install:: build
	mkdir -p $(ROOT)/$(PKGROOT)/images
	mkdir -p $(ROOT)/$(PKGROOT)/stylesheet-images
	mkdir -p $(ROOT)/$(PKGROOT)/examples
	install -ma+r index.pdf 	$(ROOT)/$(PKGROOT)/$(NAME).pdf
	install -ma+r *.html    	$(ROOT)/$(PKGROOT)/
	install -ma+r images/{*.png,*.gif}	$(ROOT)/$(PKGROOT)/images/
	install -ma+r stylesheet-images/{*.gif,*.png} \
		$(ROOT)/$(PKGROOT)/stylesheet-images/
	install -ma+r examples/*.sh	$(ROOT)/$(PKGROOT)/examples/
	install -ma+r rocks.css $(ROOT)/$(PKGROOT)/


clean::
	rm -f *.html
	rm -f index.pdf


