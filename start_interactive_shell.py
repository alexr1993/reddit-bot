## This file is a part of ref bot, credit to some guy on stack overflow,
#  this is useful for diagnosing stuff after running a script

## doesn't seem to work with the variables when imported from here...

def start_interactive_shell():
	## start interactive shell
	import readline # optional, will allow Up/Down/History in the console
	import code
	vars = globals().copy()
	vars.update(locals())
	shell = code.InteractiveConsole(vars)
	shell.interact()