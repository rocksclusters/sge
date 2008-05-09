ROLL	= sge
NAME    = roll-$(ROLL)-usersguide
RELEASE = 0

SUMMARY_COMPATIBLE      = $(VERSION)
SUMMARY_MAINTAINER      = Rocks Group
SUMMARY_ARCHITECTURE    = i386, x86_64

ROLL_REQUIRES           = base hpc kernel os1 os2 sge
ROLL_CONFLICTS          = pbs

