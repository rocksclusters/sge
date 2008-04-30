#! /opt/rocks/bin/python
#
# $RCSfile: install-qmaster.py,v $
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
# $Log: install-qmaster.py,v $
# Revision 1.14  2008/03/06 23:41:58  mjk
# copyright storm on
#
# Revision 1.13  2007/06/23 04:04:01  mjk
# mars hill copyright
#
# Revision 1.12  2006/09/11 22:50:17  mjk
# monkey face copyright
#
# Revision 1.11  2006/08/10 00:12:00  mjk
# 4.2 copyright
#
# Revision 1.10  2006/01/16 06:49:14  mjk
# fix python path for source built foundation python
#
# Revision 1.9  2005/10/12 18:10:56  mjk
# final copyright for 4.1
#
# Revision 1.8  2005/09/16 01:04:34  mjk
# updated copyright
#
# Revision 1.7  2005/08/08 21:25:02  mjk
# foundation
#
# Revision 1.6  2005/05/24 21:23:50  mjk
# update copyright, release is not any closer
#
# Revision 1.5  2004/03/25 03:16:25  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.4  2003/12/15 20:17:59  mjk
# relative paths
#
# Revision 1.3  2003/12/15 20:11:44  mjk
# - Created SGE_ARCH to find sge binaries
# - Removed more hard paths
#
# Revision 1.2  2003/12/15 19:31:04  mjk
# missed a path change
#
# Revision 1.1  2003/09/16 19:54:24  mjk
# *** empty log message ***
#

import sys
import os
import string
import socket
import rocks.sql
import pexpect


class App(rocks.sql.Application):

	def __init__(self, argv):
		rocks.sql.Application.__init__(self, argv)
		self.usage_name		= 'Install SGE QMaster'
		self.usage_version	= '@VERSION@'
		self.logFile		= None

		# Add application flags to inherited flags
		self.getopt.s.extend([('l:', 'file')])

		
	def parseArg(self, c):
		if rocks.sql.Application.parseArg(self, c):
			return 1
		elif c[0] == '-l':
			self.logFile = c[1]
		return 1
		

	def run(self):
                self.connect()
                
		info = {}
	        self.execute('select component,value from app_globals '
			     'where service="Info" and membership=0')
		for component,value in self.fetchall():
			info[component] = value

		kickstart = {}
	        self.execute('select component,value from app_globals '
			     'where service="Kickstart" and membership=0')
		for component,value in self.fetchall():
			kickstart[component] = value

                # Change the hostname of the frontend to the name of
                # the private NIC.  This insures SGE gets configured
                # for use w/in the cluster.
                
                pubName  = socket.gethostname()
                privName = socket.gethostbyaddr(kickstart['PrivateAddress'])[0]
                os.system('/bin/hostname %s' % privName)

		try:
			self.install('./install_qmaster')
		except Exception, msg:
			print
			print 'error - could not install sge', msg

		try:
			self.createAliases(pubName, privName)
		except Exception, msg:
			print
			print 'error -could not create host aliases', msg
                
                # Set the hostname back to what is was before we
                # changed it.
                
                os.system('/bin/hostname %s' % pubName)
                sys.exit(0)


	def createAliases(self, publicHostname, privateHostname):

		file = open('./default/common/host_aliases', 'w')
		file.write('%s %s\n' % (privateHostname, publicHostname))
		file.close()


        def install(self, cmd):

		child = pexpect.spawn(cmd)
				
		if self.logFile:
			file = open(self.logFile, 'w')
			child.setlog(file)
		else:
			child.setlog(sys.stdout)
		
		child.expect('<RETURN>')
		child.sendline()

		child.expect('installation settings')
		child.sendline('y')
		
		child.expect('setting file permissions')
		child.sendline('n')

		child.expect('<RETURN>')
		child.sendline()
		child.expect('<RETURN>')
		child.sendline()

		child.expect('hostname resolving method')
		child.sendline()
		child.expect('<RETURN>')
		child.sendline()

		child.expect('Please enter a range >>')
		child.sendline('20000-20100')
		child.expect('<RETURN>')
		child.sendline()

		child.expect('<RETURN>')
		child.sendline()

		child.expect('<RETURN>')
		child.sendline()

		child.expect('Grid Engine startup script')
		child.sendline()
		child.expect('<RETURN>')
		child.sendline()

		child.expect('<RETURN>')
		child.sendline()

		child.expect('Adding Grid Engine hosts')
		child.sendline()
		child.sendline()
		child.expect('<RETURN>')
		child.sendline()

		child.expect('<RETURN>')
		child.sendline('')

		child.expect('Grid Engine messages')
		child.sendline('')
		
		child.expect(pexpect.EOF)
		child.close()
		if self.logFile:
			file.close()



app = App(sys.argv)
app.parseArgs()
app.run()

