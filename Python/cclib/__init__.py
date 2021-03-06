#
# CCLib_proxy Interface Library for High-Level operations
# Copyright (c) 2014 Ioannis Charalampidis
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# Import everything from CCDebugger
from cclib.ccdebugger import *
from cclib.cchex import *

def getOptions(shortDesc, argHelp="", hexIn=False, hexOut=False, port=True, **kwargs):
	"""
	Reusable function to collect command-line options.
	"""
	import getopt
	import sys
	import os

	values = { 'enter': False }
	required = []
	arguments = []
	arguments.append( ('h', 'help', 'Display this help screen' ) )
	arguments.append( ('E', 'enter', 'Enter debug mode if not debugging already' ) )
	arg_help = "[-h|--help] [-E|--enter]"

	# Append some other options
	if hexIn:
		values['in'] = None
		arg_help += " [-i|--in=<hex file>]"
		arguments.append( ('i:', 'in=', 'Specify the hex file to read from' ) )
		required.append('in')
	if hexOut:
		values['out'] = None
		arg_help += " [-o|--out=<hex file>]"
		arguments.append( ('o:', 'out=', 'Specify the hex file to write to' ) )
		required.append('out')
	if port:
		values['port'] = os.environ.get("CC_SERIAL", None)
		arg_help += " [-p|--port=<serial>]"
		arguments.append( ('p:', 'port=', 'Specify the serial port to use (defaults to CC_SERIAL variable)' ) )
		required.append('port')

	# New line
	if len(kwargs) > 0:
		arg_help += "\n" + (" " * (7 + len(sys.argv[0])))

	# Append custom keyword arguments
	for k,v in kwargs.iteritems():
		if (v[0] == ":"):
			values[k] = None
			arg_help += " [-%s|--%s=]" % (k[0], k)
			arguments.append( (k[0]+':', k+'=', v[1:]) )
		else:
			values[k] = False
			arg_help += " [-%s|--%s]" % (k[0], k)
			arguments.append( (k[0], k, v) )

	# Parse options
	try:
		opts, args = getopt.getopt(
			sys.argv[1:], "".join(map(lambda v: v[0], arguments)), 
			map(lambda v: v[1], arguments) )
	except getopt.GetoptError as err:
		print "ERROR: %s" % str(err) 
		print shortDesc
		print "Usage: %s %s %s" % (sys.argv[0], arg_help, argHelp)
		print ""
		for a in arguments:
			if a[0][-1] == ':':
				args = "-%s,--%s=" % (a[0][:-1], a[1][:-1])
				print " %20s %s" % (args, a[2])
			else:
				args = "-%s,--%s" % (a[0], a[1])
				print " %20s %s" % (args, a[2])
		print ""
		sys.exit(2)

	# Parse options
	for o, v in opts:
		if o in ("-h", "--help"):
			print shortDesc
			print "Usage: %s %s %s" % (sys.argv[0], arg_help, argHelp)
			print ""
			for a in arguments:
				if a[0][-1] == ':':
					args = "-%s,--%s=" % (a[0][:-1], a[1][:-1])
					print " %20s %s" % (args, a[2])
				else:
					args = "-%s,--%s" % (a[0], a[1])
					print " %20s %s" % (args, a[2])
			print ""
			sys.exit()
		else:
			# Process arguments
			found = False
			for a in arguments:
				if a[0][-1] == ':':
					test = ('-%s' % a[0][:-1], '--%s' % a[1][:-1])
					if o in test:
						values[a[1][:-1]] = v
						found = True
				else:
					test = ('-%s' % a[0], '--%s' % a[1])
					if o in test:
						values[a[1]] = True
						found = True

			# Check missing
			if not found:
				print "ERROR: Unknown parameter %s" % o
				sys.exit(1)

	# Validate input
	if port and not values['port']:
		print shortDesc
		print "ERROR: Please specify a serial port either with the CC_SERIAL environment variable or with the --port argument!"
		sys.exit(1)
	for k in required:
		if not values[k]:
			print shortDesc
			print "ERROR: Missing argument '-%s', try %s --help for more details" % (k, sys.argv[0])
			sys.exit(1)

	# Include raw args
	values['args'] = args
	return values

