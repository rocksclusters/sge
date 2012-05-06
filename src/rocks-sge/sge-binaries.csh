#!/bin/csh
#
# $Id: sge-binaries.csh,v 1.15 2012/05/06 05:49:42 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
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
#
# $Log: sge-binaries.csh,v $
# Revision 1.15  2012/05/06 05:49:42  phil
# Copyright Storm for Mamba
#
# Revision 1.14  2012/04/30 16:59:03  phil
# in only add to path if not already there.
#
# Revision 1.13  2011/07/23 02:31:36  phil
# Viper Copyright
#
# Revision 1.12  2010/09/07 23:53:25  bruno
# star power for gb
#
# Revision 1.11  2010/07/19 23:18:28  anoop
# Put sge path after others in the PATH variable
#
# Revision 1.10  2009/05/01 19:07:22  mjk
# chimi con queso
#
# Revision 1.9  2008/10/18 00:56:14  mjk
# copyright 5.1
#
# Revision 1.8  2008/03/06 23:41:58  mjk
# copyright storm on
#
# Revision 1.7  2007/06/23 04:04:01  mjk
# mars hill copyright
#
# Revision 1.6  2006/09/11 22:50:16  mjk
# monkey face copyright
#
# Revision 1.5  2006/09/05 21:59:17  anoop
# Main change -
#
# Modifications to a lot of XML files. I apologize if people feel that I've
# stepped on someone else's toes here, but right now, the MANPATH variable is
# causing a bit of a headache and needs to be rethought. So all additions to
# the MANPATH variable are done via the /etc/man.config file.
#
# Please do not write shell scripts and profile.d files setting the MANPATH variable present
# as this would override the /etc/man.config file, and most man pages will not be
# available to you.
#
# Smaller changes -
#
# Refreshing packages in the xena roll. Development of xena halted for the next few weeks atleast
# Change the python version number that ganglia-python uses.
# Note added to NCBI Blast regarding upgrades in the future.
#
# Revision 1.4  2006/08/10 00:12:00  mjk
# 4.2 copyright
#
# Revision 1.3  2005/10/12 18:10:56  mjk
# final copyright for 4.1
#
# Revision 1.2  2005/09/16 01:04:33  mjk
# updated copyright
#
# Revision 1.1  2005/08/24 23:34:44  bruno
# update to sge6
#
# Revision 1.7  2005/06/24 01:36:38  tsailm
# Up the sge6 release number
#
# Revision 1.6  2005/06/23 23:14:09  tsailm
# Left out LD_LIBRARY_PATH
#
# Revision 1.5  2005/06/17 07:51:57  tsailm
# Fix post scripts for sge6u4
#
# Revision 1.4  2005/05/24 21:23:52  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/03/30 09:58:00  tsailm
# Added back SGE_ARCH.
#
# Revision 1.2  2005/03/29 05:07:06  tsailm
# Cleanup for cvs log tag
#


# Modified from $SGE_ROOT/default/common/settings.csh
setenv SGE_ROOT /opt/gridengine
setenv SGE_ARCH `$SGE_ROOT/util/arch`
set DEFAULTMANPATH = `$SGE_ROOT/util/arch -m`
set MANTYPE = `$SGE_ROOT/util/arch -mt`

setenv SGE_CELL default
setenv SGE_QMASTER_PORT 536
setenv SGE_EXECD_PORT 537


set BIN=${SGE_ROOT}/bin/${SGE_ARCH}

if ( -d ${BIN}  ) then
	echo ${PATH} | /bin/grep -q ${BIN} 
	if ( $? != 0) then
        	setenv PATH "${PATH}:${BIN}"
	endif
endif

set shlib_path_name = `$SGE_ROOT/util/arch -lib`
if ( `eval echo '$?'$shlib_path_name` ) then
   set old_value = `eval echo '$'$shlib_path_name`
   setenv $shlib_path_name "$SGE_ROOT/lib/$SGE_ARCH":"$old_value"
else
   setenv $shlib_path_name $SGE_ROOT/lib/$SGE_ARCH
endif
unset DEFAULTMANPATH MANTYPE shlib_path_name
