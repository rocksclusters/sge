NAME		= SGE
VERSION		= 6.2u5p2
RELEASE		= 1
ifeq ($(strip $(VERSION.MAJOR)), 5)
PATCHDIR        = patch-files-5
else
PATCHDIR        = patch-files
endif 
