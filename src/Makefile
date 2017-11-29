# $Id: Makefile,v 1.18 2012/11/27 00:49:30 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWindwer)
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
# Revision 1.18  2012/11/27 00:49:30  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.17  2012/05/06 05:49:42  phil
# Copyright Storm for Mamba
#
# Revision 1.16  2011/07/23 02:31:35  phil
# Viper Copyright
#
# Revision 1.15  2010/09/07 23:53:25  bruno
# star power for gb
#
# Revision 1.14  2009/05/01 19:07:22  mjk
# chimi con queso
#
# Revision 1.13  2008/11/30 19:32:48  anoop
# Added support for SGE on Solaris
#
# Revision 1.12  2008/10/18 00:56:13  mjk
# copyright 5.1
#
# Revision 1.11  2008/03/06 23:41:57  mjk
# copyright storm on
#
# Revision 1.10  2007/06/23 04:04:00  mjk
# mars hill copyright
#
# Revision 1.9  2006/09/11 22:50:15  mjk
# monkey face copyright
#
# Revision 1.8  2006/08/10 00:11:59  mjk
# 4.2 copyright
#
# Revision 1.7  2005/10/12 18:10:54  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:04:31  mjk
# updated copyright
#
# Revision 1.5  2005/05/24 21:23:48  mjk
# update copyright, release is not any closer
#
# Revision 1.4  2004/03/25 03:16:22  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.3  2003/11/05 06:32:16  mjk
# jobmanager build and is part of roll
#
# Revision 1.2  2003/10/29 20:26:14  mjk
# no globus for now
#
# Revision 1.1  2003/09/15 22:43:56  mjk
# *** empty log message ***
#
# Revision 1.2  2003/08/27 23:10:55  mjk
# - copyright update
# - rocks-dist uses getArch() fix the i686 distro bug
# - ganglia-python spec file fixes (bad service start code)
# - found some 80col issues while reading code
# - WAN ks support starting
#
# Revision 1.1  2003/07/30 22:24:25  mjk
# *** empty log message ***
#

-include $(shell $(ROCKSROOT)/bin/arch).mk
-include $(shell $(ROCKSROOT)/bin/os).mk

default: pkg

copyright rpm pkg clean::
	for i in $(SRCDIRS) ; do \
		(cd $$i; $(MAKE) $@) ; \
	done
