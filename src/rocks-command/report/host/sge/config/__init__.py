# $Id: __init__.py,v 1.2 2010/09/07 23:53:25 bruno Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# $Log: __init__.py,v $
# Revision 1.2  2010/09/07 23:53:25  bruno
# star power for gb
#
# Revision 1.1  2010/03/25 00:31:13  bruno
# plug sge into the login appliance
#
#

import rocks.commands

common_conf = """SGE_ROOT="/opt/gridengine"
SGE_QMASTER_PORT="536"
SGE_EXECD_PORT="537"
CELL_NAME="default"
ADMIN_USER=""
QMASTER_SPOOL_DIR="/opt/gridengine/default/spool/qmaster"
EXECD_SPOOL_DIR="/opt/gridengine/default/spool"
GID_RANGE="20000-20100"
SPOOLING_METHOD="classic"
DB_SPOOLING_SERVER="none"
DB_SPOOLING_DIR="/opt/gridengine/default/spooldb"
ADMIN_HOST_LIST=""
SGE_ENABLE_SMF="false"
EXECD_SPOOL_DIR_LOCAL="/opt/gridengine/default/spool"
HOSTNAME_RESOLVING="true"
SHELL_NAME="ssh"
DEFAULT_DOMAIN="none"
ADMIN_MAIL="none"
ADD_TO_RC="true"
SET_FILE_PERMS="true"
RESCHEDULE_JOBS="wait"
SCHEDD_CONF="1"
SHADOW_HOST=""
EXEC_HOST_LIST_RM=""
REMOVE_RC="true"
WINDOWS_SUPPORT="false"
WIN_ADMIN_NAME="Administrator"
"""

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.report.command):
	"""
	Outputs the SGE configuration file for a host.

	<arg type='string' name='host'>
	One host name.
	</arg>

	<example cmd='report host sge config compute-0-0'>
	Output the SGE configuration for compute-0-0.
	</example>
	"""

	def run(self, params, args):

		self.beginOutput()
		
		for host in self.getHostnames(args):
			osname = self.db.getHostAttr(host, 'os')
			f = getattr(self, 'run_%s' % osname)
			f(host)
			
		self.endOutput(padChar='')

	def run_sunos(self, host):
		#
		# stub
		#
		return
 
	def run_linux(self, host):
		f = '/opt/gridengine/util/install_modules/sge_host_config.conf'
		self.addOutput(host, '<file name="%s">' % f)

		self.addOutput(host, common_conf)

		submit_host = self.db.getHostAttr(host, 'submit_host')
		exec_host = self.db.getHostAttr(host, 'exec_host')
		sge_cluster_name = self.db.getHostAttr(host,
			'Kickstart_PrivateHostname')

		if submit_host == 'true':
			self.addOutput(host, 'SUBMIT_HOST_LIST="`hostname`"')
		if exec_host == 'true':
			self.addOutput(host, 'EXEC_HOST_LIST="`hostname`"')

		self.addOutput(host, 'SGE_CLUSTER_NAME="%s"' %
			(sge_cluster_name))

		self.addOutput(host, '</file>')
