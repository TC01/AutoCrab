"""
Autocrab Core; the code that gets ran by the script.
"""

import os
import shutil
import sys

from AutoCrab.AutoCrab2 import aliases
from AutoCrab.AutoCrab2 import crabutil
from AutoCrab.AutoCrab2 import commands

def isValidCommand(command):
	"""isValidCommand returns 0 if the command is not a valid autocrab command,
	and 1 otherwise."""
	valid = False
	if command in aliases.cfg_commands.keys():
		valid = True
	if command in aliases.dir_commands.keys():
		valid = True
	if command in commands.plugin_commands.keys():
		valid = True
	return valid

def getCommandType(command):
	"""This method returns an enum of sorts depending on the type of command."""
	if command in aliases.cfg_commands.keys():
		return aliases.CFG_COMMAND
	if command in aliases.dir_commands.keys():
		return aliases.DIR_COMMAND
	if command in commands.plugin_commands.keys():
		return aliases.PLUGIN_COMMAND
	return 0

def doAutoCrab(command, recursive=False):
	"""Run the actual autocrab method."""

	# for now, use os.getcwd()
	for path, dirs, files in os.walk(os.getcwd()):
		if path != os.getcwd() and not recursive:
			continue

		if recursive and crabutil.isCrabDirectory(path):
			continue

		if getCommandType(command) == aliases.CFG_COMMAND:
			for file in files:
				if not crabutil.isCrabConfig(file):
					continue
				os.system(crabline + file)

		for dir in dirs:
			# Check if the inside is set up like a crab file.
			if not crabutil.isCrabDirectory(os.path.join(path, dir)):
				continue
			print "Processing " + dir
			
			if getCommandType(command) == aliases.PLUGIN_COMMAND:
				results = commands.plugin_commands[command].autocrab(os.path.join(path, dir))
			else:
				# Construct a crab command line.
				crabline = aliases.crab_command + " "
				if getCommandType(command) == aliases.CFG_COMMAND:
					crabline += aliases.cfg_commands[command] + " -cfg "
				elif getCommandType(command) == aliases.DIR_COMMAND:
					crabline += aliases.dir_commands[command] + " -c "
				os.system(crabline + os.path.join(path, dir))

			#	results = valid_functions[command](os.path.join(path, dir))

