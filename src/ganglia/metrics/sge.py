#!/opt/rocks/bin/python
#
# A metric for Greceptor that publishes some SGE 6
# (Queue system) metrics through Ganglia.
# For use with Rocks Ganglia addon pages. 
#
# Authors:
#	Federico Sacerdoti 2005
#	Emir Imamagic 2005
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
# $Log: sge.py,v $
# Revision 1.25  2008/06/24 19:18:28  bruno
# fix for getting user submitted jobs into the 'Job Queue' display on the
# ganglia web browser.
#
# also, a fix to correct the number of total slots as reported by SGE.
#
# Revision 1.24  2008/03/06 23:41:57  mjk
# copyright storm on
#
# Revision 1.23  2007/06/23 04:04:00  mjk
# mars hill copyright
#
# Revision 1.22  2006/09/18 21:45:50  anoop
# Small changes to ganglia and SGE roll.
# sge.py now parses the date in the right format.
# queue.py does not report a running time if the job not yet started.
#
# Revision 1.21  2006/09/11 22:50:16  mjk
# monkey face copyright
#
# Revision 1.20  2006/08/10 00:11:59  mjk
# 4.2 copyright
#
# Revision 1.19  2006/01/16 06:49:14  mjk
# fix python path for source built foundation python
#
# Revision 1.18  2005/10/12 18:10:54  mjk
# final copyright for 4.1
#
# Revision 1.17  2005/10/03 20:58:46  bruno
# if the sge service is up and running, then self.parser.parse() will
# throw an exception. an exception will cause greceptor to permantently disable
# this metric. so, if SGE comes back up in the future, then we still will
# not get any SGE job info reported through ganglia.
#
# this fix catches the exception, so this metric will not be disabled with the
# SGE service is down.
#
# Revision 1.16  2005/09/30 22:53:27  bruno
# move to foundation
#
# Revision 1.15  2005/09/20 22:09:24  bruno
# updated to foundation
#
# included patch from sacerdoti
#
# Revision 1.6  2005/09/16 01:04:39  mjk
# updated copyright
#
# Revision 1.5  2005/05/24 21:23:52  mjk
# update copyright, release is not any closer
#
# Revision 1.4  2005/05/24 18:03:34  fds
# Support for SGE task arrays by Emir Imamagic.
#
# Revision 1.3  2005/04/27 19:01:49  fds
# Monitor for SGE6 queues - xml based. First design.
#
# Revision 1.2  2005/03/29 05:07:05  tsailm
# Cleanup for cvs log tag
#


import os
import sys
import time
import gmon.events
# Our MPD-style name list encoder.
import gmon.encoder
import rocks.util
import xml.sax


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
			
	def __str__(self):
		return "Queue %s: total slots=%s" % \
			(self.name, self.slots)
		


class SGE6(gmon.events.Metric):
	"""Monitors the SGE 6 queues using Ganglia. Has a simple view of 
	the cluster: a single shared Queue containing all jobs."""
	
	# How often we publish (in sec), on average.
	freq = 30
	debug = 0
	
	def __init__(self, app):
		# Schedule every few seconds on average.
		gmon.events.Metric.__init__(self, app, self.freq)
		self.jobs = {}
		self.queues = {}
		self.parser = xml.sax.make_parser()
		self.handler = QstatHandler()
		self.parser.setContentHandler(self.handler)
		
		
	def printJobs(self):
		"Prints a summary of jobs and queues to stdout."
		
		print "Jobs"
		for id,j in self.handler.getJobs().items():
			print " %s: %s" % (id, j)
		
		print "Queues"
		for q in self.handler.getQueues():
			print " ", q	
			
					
	def parseLocalFile(self, filename):
		"For testing, parses a static file of xml."
		f = open(filename, 'r')
		self.parser.parse(f)
		f.close()	
		self.printJobs()
		

	def dmax(self):
		return self.freq * 3

		
	def schedule(self, sched):

		self.qstat = self.which("qstat")

		if self.qstat and self.qstat.count('gridengine'):
			gmon.events.Metric.schedule(self, sched)
			return 1
		else:
			self.info("SGE qstat cmds not in our path, exiting.")
			return 0


	def findjobs(self):
		"Collect info in all jobs in queue."

		self.parser.reset()
		self.handler.reset()
		
		f = os.popen("%s -f -u \* -xml" % (self.qstat))

		try:
			self.parser.parse(f)
			self.jobs = self.handler.getJobs()
			self.queues = self.handler.getQueues()
		except:
			pass

		f.close()
		
		return
		

	def run(self):
		"Publishes global and per-job batch queue state."

		self.findjobs()
		
		# Publish current queue state.
		for q in self.queues:
			for name, val in q.getState().items():
				self.publish(name, val, dmax=(self.dmax() * 4))

		# Publish current job info.
		for jobid, j in self.jobs.items():
			name = j.getName()
			value = str(j)
			
			#print name, value
			self.publish(name, value)



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
		self.thisqueue.slots = int(self.text) - self.slots_used
		
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
		

def initEvents():
	return SGE6
	

#
# Testing code
#
if __name__ == "__main__":
	print "Testing SGE6 ganglia monitor"
	app = Job()
	sge = SGE6(app)
	if len(sys.argv) > 1:
		xmlfile = sys.argv[1]
		print "Parsing qstat xml from file %s...\n" % xmlfile
		sge.parseLocalFile(xmlfile)
	else:
		print "Parsing qstat output..."
		if not sge.schedule(sge):
			sys.exit(1)
		sge.run()
		sge.printJobs()
		

