import optparse

class AutocrabCommand:
	
	def __init__(name, parser):
		this.parser = parser
		this.name = name
		
	def getName():
		return this.name
	
	def getHelpText():
		return this.parser.format_help()
	
	def runCommand(argv=None):
		# So how *will* this work? Uncertain.
		(opts, args) = parser.parse_args(argv)