SRCDIRS = `find . -type d -maxdepth 1 \
	-not -name CVS \
	-not -name globus-sge \
	-not -name sun_sge \
	-not -name sge	\
	-not -name .`
