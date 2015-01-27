import imp
import os
import sys

# Code taken from me (Ben Rosser), elsewhere:
# https://bitbucket.org/TC01/hex/raw/657d87612d93f29870db5b24bf8f0eeb6348a642/hexlib/plugins/__init__.py?at=master

plugin_commands = {}

def loadCommands(toLoad, useAll=False):
	# Get a list of all possible command names
	location = os.path.join(getScriptLocation())
	names = []
	for path, dirs, files in os.walk(location):
		if path == location:
			for filename in files:
				if not (".pyc" in filename or "__init__" in filename):
					filename = filename[:-len(".py")]
					names.append(filename)
					
	# Now, use imp to load all the commands we specified
	global plugin_commands
	for name in names:
		if useAll or name in toLoad:
			try:
				test = sys.modules[name]
			except KeyError:
				fp, pathname, description = imp.find_module(name, __path__)
				try:
					command = imp.load_module(name, fp, pathname, description)
					plugin_commands[name] = command
				finally:
					if not fp is None:
						fp.close()

def getScriptLocation():
	"""Helper function to get the location of a Python file."""
	location = os.path.abspath("./")
	if __file__.rfind("/") != -1:
		location = __file__[:__file__.rfind("/")]
	return location


# Actually *load* commands.
loadCommands([], True)
