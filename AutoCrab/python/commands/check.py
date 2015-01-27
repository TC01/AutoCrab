# The 'autocrab check' plugin command.

import os
import shutil

from AutoCrab.AutoCrab import aliases
from AutoCrab.AutoCrab import crabutil

def autocrab(dir):
	"""Creates a CrabStats object by running crab -status -get all
		and summarizing the results."""

	crabline = aliases.crab_command + " " + aliases.dir_commands['status'] + " "
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

	results = (totalJobs, passedJobs)
	if results[0] != results[1]:
		print dir + ": Only " + str(results[1]) + " out of " + str(results[0]) + " jobs are in exit code 0."
	else:
		print dir + ": All jobs ran and have returned with exit code 0."
