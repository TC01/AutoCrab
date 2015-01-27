"""
Autocrab Core; the code that gets ran by the script.
"""

import os
import shutil
import sys

from AutoCrab.AutoCrab import aliases
from AutoCrab.AutoCrab import crabutil

# These probably shouldn't be here.


# Functions; should be spun off into another library.
def autocrabDelete(dir):
	config = crabutil.getCrabConfig(dir)
	with open(config) as configFile:
		configText = configFile.read()
		remoteDir = configText[configText.find("user_remote_dir"):]
		remoteDir = remoteDir[remoteDir.find("=") + 1:].lstrip()
		remoteDir = remoteDir[:remoteDir.find("\n")]
		# Hardcode /eos/uscms in here.
		remote = "/eos/uscms/" + remoteDir
		try:
			print "Deleting remote directory with previous run: " + remote
			shutil.rmtree(remote)
		except:
			pass

	print "Deleting local crab directory: " + dir
	shutil.rmtree(dir)

def autocrabCheck(dir):
	"""Creates a CrabStats object by running crab -status -get all
		and summarizing the results."""

	crabline = valid_commands['status']
	# We need to run twice, otherwise we can't guarantee that "get" ran.
	os.system(crabline + dir + "> /dev/null")
	os.system(crabline + dir + "> /dev/null")

	# Now access crab.log
	with open(crabutil.getCrabLog(dir)) as logfile:
		logtext = logfile.read()
		logtext = logtext[logtext.rfind("Checking the status of all jobs: please wait"):]
		totalJobs = logtext[:logtext.find("Total Jobs")].rstrip()
		totalJobs = totalJobs[totalJobs.rfind(" "):].lstrip()
		passedJobs = logtext[:logtext.find("Jobs with Wrapper Exit Code : 0")].rstrip()
		passedJobs = passedJobs[passedJobs.rfind(" "):].lstrip()
		try:
			totalJobs = int(totalJobs)
			passedJobs = int(passedJobs)
		except:
			print "Error: something went wrong trying to summarize results."

	return totalJobs, passedJobs

valid_functions = {	'delete': autocrabDelete,
					'check': autocrabCheck}

# 

def isValidCommand(command):
	"""isValidCommand returns 0 if the command is not a valid autocrab command,
	and 1 otherwise."""
	valid = False
	if command in aliases.cfg_commands.keys():
		valid = True
	if command in aliases.dir_commands.keys():
		valid = True
	return valid

def getCommandType(command):
	"""This method returns an enum of sorts depending on the type of command."""
	if command in aliases.cfg_commands.keys():
		return aliases.CFG_COMMAND
	if command in aliases.dir_commands.keys():
		return aliases.DIR_COMMAND
	return 0

def doAutoCrab(command, recursive):
	function = False
	if command in valid_functions.keys():
		function = True

	# Command specific tracking data. Need a way to get rid of this. Or do we?
	# Modularization, modularization, modularization.
	failed = False
	if command == "check":
		print "Checking current status of all jobs."

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
			if not function:
				# Construct a crab command line.
				crabline = aliases.crab_command + " "
				if getCommandType(command) == aliases.CFG_COMMAND:
					crabline += aliases.cfg_commands[command] + " -cfg "
				elif getCommandType(command) == aliases.DIR_COMMAND:
					crabline += aliases.dir_commands[command] + " -c "
				os.system(crabline + os.path.join(path, dir))
			else:
				results = valid_functions[command](os.path.join(path, dir))
				if command == "check":
					if results[0] != results[1]:
						print dir + ": Only " + str(results[1]) + " out of " + str(results[0]) + " jobs are in exit code 0."
						failed = True

	if command == "check" and not failed:
		print "All jobs ran and have returned with exit code 0."
