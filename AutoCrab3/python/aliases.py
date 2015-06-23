"""
Autocrab commands that are just aliases for a set of
crab commands. No complicated code is needed.
"""

crab_command = "crab"

# NOTE: as of CRAB3, some autocrab commands are deprecated.
# I've chosen to support 'create' and 'submit and have them both
# do the same thing. Others have been removed for now.

# Commands that crab should run with the -cfg option.
cfg_commands = {	'create':'submit',
					'submit':'submit'
					}

# Commands that should be run with the -c option.
dir_commands = {	'status':'status', 
					'kill':'kill',
					'resubmit':'resubmit', 
					}

# Some definitions. It seems I've picked up the "enum" "design" "pattern"...
CFG_COMMAND = 1
DIR_COMMAND = 2
PLUGIN_COMMAND = 3
