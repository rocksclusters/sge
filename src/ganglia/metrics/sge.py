#!/opt/rocks/bin/python
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# $Log: sge.py,v $
# Revision 1.29  2009/07/10 21:03:51  bruno
# add queue metrics back
#
#

import os
import sys
import time
import xml.sax
sys.path.append('/opt/rocks/lib/python2.4/site-packages')
import gmon.events
# Our MPD-style name list encoder.
import gmon.encoder
import rocks.util


class Job:
	def __init__(self):
		self.user = 'unknown'
		self.size = 0
		self.name = 'unknown'
		self.state = 'u'
		self.id = 0
		self.started = 0
		self.nodes = []
		self.pe = 'unknown'
		self.states = { 
			'r': 'Running', 't': 'Transfering', 
			'R': 'Restarted', 's': 'Suspended',
			'S': 'Suspended', 'T': 'Threshold',
			'qw': 'Queue Wait',
			'Eqw': 'Queue Wait (Error)',
			'u': 'Unknown'
			}
		# Used to compact node name lists.
		self.e = gmon.encoder.Encoder()
		
		
	def setState(self, s):
		if s in self.states:
			self.state = s
		else:
			self.state = 'u'
			
	def getState(self):
		return self.states[self.state]
	
		
	def getName(self):
		"Name for ganglia metric"
		return "queue-job-%s" % self.id
		
	def setStarted(self, s):
		# Start time is always kept in seconds.
		t = time.strptime(s, "%Y-%m-%dT%H:%M:%S")
		# Adjust for daylight savings
		t = t[:-1] + (time.daylight,)
		self.started = time.mktime(t)
		
		
	def setOwner(self, o):
		"SGE6 calls the user owner. I like owner actually"
		self.user = o
		
		
	def __str__(self):
		# Delimit with ", " so list looks good, and we can
		# have spaces in the values.
		
		if self.size == 0:
			self.size = 1
			
		value = "user=%s, P=%s, state=%s, started=%s, name=%s" \
			% (self.user, self.size, 
			self.getState(), self.started, self.name)

		if self.state in ('r','t'):
			value += ", nodes=%s" % \
				(self.e.encode(self.nodes))
		return value
		

class Queue:
	def __init__(self):
		self.slots = 0
		self.name = 'current'
		self.type = 'BIP'
		self.arch = 'unknown'

		
	def getState(self):
		return {
			'queue-state': 'P=%d' % self.slots
			}
			

class QstatHandler(rocks.util.ParseXML):
	"""Knows how to parse XML output from sge6 qstat"""
	
	def __init__(self):
		rocks.util.ParseXML.__init__(self)
		self.thisjob = None
		self.thisqueue = None
		self.reset()
		
		
	def reset(self):
		self.jobs = {}
		self.queues = []
		
	def getJobs(self):
		return self.jobs
		
	def getQueues(self):
		return self.queues
		
	def startElement_queue_info(self, name, attrs):
		"Assuming this is the beginning of a queue definition"
		self.thisqueue = Queue()
		
	def endElement_queue_info(self, name):
		self.queues.append(self.thisqueue)
		
	def startElement_name(self, name, attrs):
		"Assuming this is only the name of a node queue"
		self.text = ''
		
	def endElement_name(self, name):
		try:
			self.nodename = self.text.split('@')[1]
			self.nodename = self.nodename.split('.')[0]
		except:
			print ' warning - cannot understand node Q %s' \
				% self.text
			self.nodename = 'unknown'

	def startElement_slots_used(self, name, attrs):
		self.text = ''
	
	def endElement_slots_used(self, name):
		self.slots_used = int(self.text)
		
	def startElement_slots_total(self, name, attrs):
		self.text = ''
	
	def endElement_slots_total(self, name):
		self.thisqueue.slots = int(self.text)
		
	def startElement_job_list(self, name, attrs):
		pass
			
	def endElement_job_list(self, name):
		self.jobs[self.thisjob.id] = self.thisjob
		self.thisjob = Null()
			
	def startElement_JB_job_number(self, name, attrs):
		self.text = ''
		
	def endElement_JB_job_number(self, name):
		id = self.text
		if id in self.jobs:
			self.thisjob = self.jobs[id]
		else:
			self.thisjob = Job()
		self.thisjob.id = id
		
	def startElement_JB_name(self, name, attrs):
		self.text = ''
		
	def endElement_JB_name(self, name):
		self.thisjob.name = self.text
		
	def startElement_JB_owner(self, name, attrs):
		self.text = ''
		
	def endElement_JB_owner(self, name):
		self.thisjob.setOwner(self.text)
		
	def startElement_state(self, name, attrs):
		self.text = ''
		
	def endElement_state(self, name):
		self.thisjob.setState(self.text)
		
	def startElement_JAT_start_time(self, name, attrs):
		self.text = ''
		
	def endElement_JAT_start_time(self, name):
		self.thisjob.setStarted(self.text)
		
	def startElement_slots(self, name, attrs):
		self.text = ''
		
	def endElement_slots(self, name):
		size = int(self.text)
		self.thisjob.size += size
		if self.thisjob.state in ('r','t'):
			self.thisjob.nodes.extend([self.nodename]*size)
			
	def startElement_tasks(self,name,attrs):
		self.text = ''

	def endElement_tasks(self,name):
		task = self.text
		self.thisjob.id += "." + task

class Null:
	"""Null objects always and reliably do nothing.
	   From Python Cookbook p.211"""

	def __init__(self, *args, **kwargs): pass
	def __call__(self, *args, **kwargs): return self
	def __repr__(self): return "Null()"
	def __nonzero__(self): return 0

	def __getattr__(self, name): return self
	def __setattr__(self, name, value): return self
	def __delattr__(self, name): return self
		

def sge_queue_state_handler(name):
	totalslots = 'P=0'

	jobs = {}
	queues = {}
	parser = xml.sax.make_parser()
	handler = QstatHandler()
	parser.setContentHandler(handler)

	#
	# find jobs
	#
	f = os.popen("qstat -f -u \* -xml")

	try:
		parser.parse(f)
		jobs = handler.getJobs()
		queues = handler.getQueues()
		totalslots = 'P=%d' % handler.thisqueue.slots
	except:
		pass

	f.close()

	#
	# for the job info, make calls to gmetric
	#
	for jobid, j in jobs.items():
		name = j.getName()
		value = str(j)

		cmd = '/opt/ganglia/bin/gmetric '
		cmd += '--name="%s" ' % name
		cmd += '--value="%s" ' % value
		cmd += '--type="string" '
		cmd += '--slope=zero '
		cmd += '--dmax=120 '

		os.system(cmd)

	return totalslots


def metric_init(params):
	global descriptors

	descriptors = []

	d = {
		'name': 'queue-state',
		'call_back': sge_queue_state_handler,
		'time_max': 60,
		'value_type': 'string',
		'units': '',
		'slope': 'zero',
		'format': '%s',
		'description': 'SGE Queue State',
		'groups': 'sge'
	}

	descriptors.append(d)

	return descriptors
 
def metric_cleanup():
	'''Clean up the metric module.'''
	pass
 
#This code is for debugging and unit testing
if __name__ == '__main__':
	metric_init(None)
	for d in descriptors:
		v = d['call_back'](d['name'])
		print 'value for %s is %s' % (d['name'],  v)

