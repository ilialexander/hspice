import os, re, subprocess


def module(*args):
	if type(args[0]) == type([]):
		args = args[0]
	else:
		args = list(args)
	(output, error) = subprocess.Popen(['/usr/bin/modulecmd', 'python'] + 
			args, stdout=subprocess.PIPE).communicate()
	exec(output)

