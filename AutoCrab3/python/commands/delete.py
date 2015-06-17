# The autocrab delete plugin command.

# This also needs to be rewritten for crab3, especially the configuration parsing.
# But the deleting of local directories still works

import shutil

from AutoCrab.AutoCrab2 import crabutil

# Hardcode /eos/uscms in here.
eos_root = "/eos/uscms"

def autocrab(dir):

#"""config = crabutil.getCrabConfig(dir)
	#with open(config) as configFile:
	#	configText = configFile.read()
	#	remoteDir = configText[configText.find("user_remote_dir"):]
	#	remoteDir = remoteDir[remoteDir.find("=") + 1:].lstrip()
	#	remoteDir = remoteDir[:remoteDir.find("\n")]
	#	remote = eos_root + remoteDir
	#	try:
	#		print "Deleting remote directory with previous run: " + remote
	#		shutil.rmtree(remote)
	#	except:
	#		pass"""

	print "Deleting local crab directory: " + dir
	shutil.rmtree(dir)
