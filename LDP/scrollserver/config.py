"""
$Id$

Handle configuration setup.

All of the configuration options and information on their format are at the end
of this file.
"""
import getopt, sys, os, ConfigParser

defaultConfigFile = 'scrollserver.conf'

# These constants just make the code more readable. They refer to fields in the
# 'flatOptions' value tuples.
SECTION = 0
FUNC = 1
DEFAULT = 2

# An exception which will only be raised by this module
class ConfigError(Exception): pass

def parseConfig():
	"""
	The main entry point for this module. This function returns a
	dictionary containing a value for all of the options specified in
	configOptions. It does this by choosing, for each option, the first
	available value from
		1. The command line (--option)
		2. The config file specified in the $SCROLLSERVER_CONFIG
		environment variable.
		3. The config file specificed in the 'defaultConfigFile'
		variable.
		4. A hardcoded default from 'configOptions'.
	"""
	# First, fill in the results dictionary with all the fields we need to
	# eventually have values for. Construct the list to pass to getopts in
	# the same pass.
	result = {}
	longArgs = []
	for option in flatOptions.keys():
		result[option] = None
		if flatOptions[option][FUNC] == None:
			longArgs.append(option)
		else:
			longArgs.append('%s=' % option)
			
	# Now parse the command line.
	optlist, args = getopt.getopt(sys.argv[1:], '', longArgs)
	for opt, value in optlist:
		# Strip off the leading '--' from the option
		opt = opt[2:]
		func = flatOptions[opt][FUNC]
		if func:
			result[opt] = func(value)
		else:
			result[opt] = 1
	# It only makes sense to ask for help on the commandline, so we show it
	# here and return immediately.
	if result['help'] == 1:
		showHelp()
		return result
	
	# Look in the file in $SCROLLSERVER_CONFIG.
	filename = os.environ.get('SCROLLSERVER_CONFIG')
	if filename:
		processConfigFile(filename, result)
	
	# Look in the default config file.
	processConfigFile(defaultConfigFile, result)

	# And, finally, use the default values for anything not yet filled in.
	for option, value in result.items():
		if value == None:
			result[option] = flatOptions[option][DEFAULT]
	return result

def processConfigFile(filename, dict):
	"""
	Read the config parameters from 'filename' and for any item in 'dict'
	that has a value of None, fill in the value (if any) from the file. If
	the specified file does not exist, this function will do nothing.
	"""
	try:
		fd = open(filename)
	except IOError:
		# FIXME: display error message somehow?
		return
	cp = ConfigParser.ConfigParser()
	cp.readfp(fd)
	for section in configOptions.keys():
		if not cp.has_section(section):
			continue
		for option in configOptions[section].keys():
			if result[option] != None or not cp.has_option(section, option):
				continue
			value = cp.get(section, option)
			func = flatOptions[option][FUNC]
			if func:
				dict[option] = func(value)
			else:
				dict[option] = 1

def cacheSize(param):
	"""
	Handle strings that specify the cache size. These are just numbers,
	possibly with suffix of 'k' or 'm' or 'g' (upper- or lower-case). If
	the 'param' is badly formed (e.g. 1234mg), a ValueError exception will
	be raised.
	"""
	multipliers = {'k': 1024, 'm': 1024 * 1024, 'g': 1024 * 1024 * 1024}
	param = param.strip()
	suffix = param[-1].lower()
	if suffix in multipliers.keys():
		mult = multipliers[suffix]
		param = param[:-1]
	else:
		mult = 1
	return long(param) * mult

def showHelp():
	"""
	List all of the options and their help strings from 'configOptions'.
	"""
	sections = configOptions.keys()
	# Do the sections and the options alphabetically.
	sections.sort()
	for section in sections:
		print 'Options for %s:' % section
		options = configOptions[section].keys()
		options.sort()
		for option in options:
			print '   --%s: %s' \
			       % (option, configOptions[section][option][2])
		print


# The 'configOptions' variable describes the various options which can be
# configured. It is a dictionary of (Section, Options) mappings. The 'Section'
# key describes the area of the program to which the options correspond. It is
# also the name of a major section in the config file.
#
# The 'Options' value is another dictionary which maps configuration parameters
# to a tuple which is (conversion-function, default-value, help-string). The
# conversion function is either None (in which case the config option is 'on'
# when present and 'off' otherwise) or a function which converts a string to an
# appropriate value for later use. This can either be a builtin Python function
# (e.g. 'str' or 'int') or a custom function.
#
# Note that this dictionary needs to be defined _after_ any custom functions it
# refers to, so we put it here at the end of this module.
configOptions = {
	'scrollserver': {
		'cache-dir': (str, '/var/cache/scrollserver/',
		              'The directory where files will be cached.'),
		'cache-size': (cacheSize, 10485760, # 10 megabytes
		               'The size of the cache (k, m and g suffixes '
			       'permitted).'),
		'disable-cache': (None, 0, 'If present, disable the cache.'),
		'port': (int, 8000, 'The port to listen on.'),
		'interface': (str, '', 'The interface to listen on '
		                       '("" = all interfaces).'),
		'help': (None, 0, 'Show short description of options.'),
	},
	'xsltproc': {
		'timing': (None, 0, 'Display the time used by xsltproc.'),
	},
}

# In some cases (e.g. parsing the command line), the above format is not so
# convenient to use. So, upon module import we construct another dictionary
# which moves the options up to the top level and keeps a reference to their
# section, conversion function and default value.
flatOptions = {}
for section, optionDict in configOptions.items():
	for option, (func, default, junk) in optionDict.items():
		if flatOptions.has_key(option):
			# This option already exists, so we have a fatal error.
			first = flatOptions[option][0]
			raise ConfigError, 'Option %s exists in sections ' \
			                   '%s and %s.' % (first, section)
		flatOptions[option] = (section, func, default)

