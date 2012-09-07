NAME		= GE
VERSION		= 2011.11p1
RELEASE		= 1
ifeq ($(strip $(VERSION.MAJOR)), 5)
PATCHDIR        = patch-files-5
else
PATCHDIR        = patch-files
endif 
