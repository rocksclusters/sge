#
# insert-ethers plugin module
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# $Log: sge.py,v $
# Revision 1.24  2011/07/23 02:31:35  phil
# Viper Copyright
#
# Revision 1.23  2010/09/07 23:53:25  bruno
# star power for gb
#
# Revision 1.22  2009/05/01 19:07:22  mjk
# chimi con queso
#
# Revision 1.21  2009/03/06 22:42:11  bruno
# add and use the command: rocks report sge machines
#
# Revision 1.20  2008/10/18 00:56:14  mjk
# copyright 5.1
#
# Revision 1.19  2008/04/25 19:57:02  bruno
# speed up 'rocks sync config' by 10x
#
# Revision 1.18  2008/03/06 23:41:57  mjk
# copyright storm on
#
# Revision 1.17  2007/06/23 04:04:00  mjk
# mars hill copyright
#
# Revision 1.16  2006/09/20 19:01:33  bruno
# make sure the plugin can always find qconf
#
# Revision 1.15  2006/09/11 22:50:16  mjk
# monkey face copyright
#
# Revision 1.14  2006/09/11 18:08:14  bruno
# don't call restart() when '--batch' or '--norestart' flags are present.
#
# Revision 1.13  2006/08/10 00:12:00  mjk
# 4.2 copyright
#
# Revision 1.12  2005/10/17 19:45:50  bruno
# if in batch or norestart mode, don't call the 'added' function
#
# Revision 1.11  2005/10/12 18:10:55  mjk
# final copyright for 4.1
#
# Revision 1.10  2005/09/16 01:04:33  mjk
# updated copyright
#
# Revision 1.9  2005/09/06 23:33:05  bruno
# cleanup -- make code easier to manage.
#
# Revision 1.8  2005/08/26 19:32:00  bruno
# added a loop to check if 'qconf' successfully completed
#
# Revision 1.7  2005/08/25 20:28:16  bruno
# cleanup
#
# Revision 1.6  2005/08/24 23:34:44  bruno
# update to sge6
#
# Revision 1.7  2005/06/22 08:20:55  tsailm
# Fixes for insert-ethers plugins for sge6u4
#
# Revision 1.6  2005/06/17 07:54:02  tsailm
# insert-ethers plugin for sge6u4
#
# Revision 1.5  2005/05/27 22:34:57  fds
# Insert-ethers plugins also get node id for added(), removed().
#
# Revision 1.4  2005/05/24 21:23:52  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/04/05 09:18:51  tsailm
# The proper sge6 insert-ethers plugin
#
# Revision 1.2  2005/03/29 05:07:06  tsailm
# Cleanup for cvs log tag
#



import os
import popen2
import commands
import time
import os.path
import rocks.sql
from syslog import syslog

class Plugin(rocks.sql.InsertEthersPlugin):
	"Controls SGE when nodes are added."

	def added(self, nodename, id):
		#
		# don't execute this code if we are in 'batch' or 'norestart'
		# mode
		#
		if '--batch' in self.app.caller_args or \
				'--norestart' in self.app.caller_args:
			return

		#
		# wait until SGE can resolve the nodename
		#
		failedmsg = "can't resolve hostname"

		done = 0
		while not done:
			cmd = '. /etc/profile.d/sge-binaries.sh ; ' + \
				'qconf -ah %s' % (nodename)
			(status, output) = commands.getstatusoutput(cmd)

			commands.getstatusoutput(
				'echo "status:%s" >> /tmp/sge_install.debug' \
								% (status))
			commands.getstatusoutput(
				'echo "output:%s" >> /tmp/sge_install.debug' \
								% (output))

			if len(output) > len(failedmsg) and \
					output[0:len(failedmsg)] == failedmsg:
				done = 0
			else:
				done = 1
		return


	def update(self):
		self.restart()
		return


	def done(self):
		return


	def restart(self):
		if '--batch' in self.app.caller_args or \
				'--norestart' in self.app.caller_args:
			return

		#
		# get a list of the current admin hosts
		#
		adminhosts = []
		cmd = '. /etc/profile.d/sge-binaries.sh ; qconf -sh'
		for line in os.popen(cmd).readlines():
			adminhosts.append(line.strip())

		#
		# get a list of machines under SGE control
		#
		cmd = '/opt/rocks/bin/rocks report sge machines'
		r, w = popen2.popen2(cmd)

		for m in r.readlines():
			machine = m.strip()

			if machine not in adminhosts:
				self.added(machine, 0)

		return

