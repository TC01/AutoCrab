"""
Autocrab commands that are just aliases for a set of
crab commands. No complicated code is needed.
"""

crab_command = "crab"

# Commands that crab should run with the -cfg option.
cfg_commands = {	'create':'-create -submit',
					'createonly':'-create'
					}

# Commands that should be run with the -c option.
dir_commands = {	'submit':'-submit',
					'status':'-status -get all', 
					'resubmit':'-resubmit bad', 
					'publish':'-publish'
					}

# Some definitions. It seems I've picked up the "enum" "design" "pattern"...
CFG_COMMAND = 1
DIR_COMMAND = 2
PLUGIN_COMMAND = 3
