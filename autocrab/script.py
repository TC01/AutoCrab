#!/usr/bin/env python

import optparse
import os
import shutil
import sys

import crabutil

# Commands that are a simple wrapper around a set of crab commands.
valid_commands = {	'create':'crab -create -submit -cfg ', 
					'submit':'crab -submit -c ',
					'createonly':'crab -create -cfg ',
					'status':'crab -status -get all -c ', 
					'resubmit':'crab -resubmit bad -c ', 
					'publish':'crab -publish -c '}

# Functions; should be spun off into another library.
def autocrabDelete(dir):
	config = getCrabConfig(dir)
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
	with open(getCrabLog(dir)) as logfile:
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


def doAutoCrab(command, recursive):
	function = False
	crabline = ""
	if command in valid_commands.keys():
		crabline = valid_commands[command]
	elif command in valid_functions.keys():
		function = True

	# Command specific tracking data.
	failed = False
	if command == "check":
		print "Checking current status of all jobs."

	# for now, use os.getcwd()
	for path, dirs, files in os.walk(os.getcwd()):
		if path != os.getcwd() and not recursive:
			continue

		if recursive and isCrabDirectory(path):
			continue

		if command == "create" or command == "createonly":
			for file in files:
				if not isCrabConfig(file):
					continue
				os.system(crabline + file)

		for dir in dirs:
			# Check if the inside is set up like a crab file.
			if not isCrabDirectory(os.path.join(path, dir)):
				continue
			print "Processing " + dir
			if not function:
				os.system(crabline + os.path.join(path, dir))
			else:
				results = valid_functions[command](os.path.join(path, dir))
				if command == "check":
					if results[0] != results[1]:
						print dir + ": Only " + str(results[1]) + " out of " + str(results[0]) + " jobs are in exit code 0."
						failed = True

	if command == "check" and not failed:
		print "All jobs ran and have returned with exit code 0."

def main():
	parser = optparse.OptionParser()
	parser.add_option("-r", "--recursive", dest="recursive", action="store_true", help="The DBS to look up datasets in.")
	(opts, args) = parser.parse_args()

	for arg in args:
		if arg not in valid_commands.keys() and arg not in valid_functions.keys():
			print "Error: unrecognized autocrab command."
		else:
			doAutoCrab(arg, opts.recursive)

if __name__ == '__main__':
	main()
