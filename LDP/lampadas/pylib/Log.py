#!/usr/bin/python

"""
Lampadas Log Module

This module generates the system log for Lampadas.
"""

# Modules ##################################################################


class Log:
	"""
	Write to the system log.
	"""

	import Config

	Config = Config.Config()

	def __call__(self, level, message):
		self.Write(level, message)

	def Write(self, level, message):
		if self.Config.LogLevel >= level:
			self.log = open(self.Config.LogFile, 'a+')
			self.log.write(message + "\n")
			self.log.close
		if self.Config.LogConsole > 0:
			print message

	def Truncate(self):
		self.log = open(self.Config.LogFile, 'w+')
		self.log.close

if __name__ == "__main__":
	Log = Log()
	Log(1, 'level 1')
	Log(2, 'level 2')
	Log(3, 'level 3')

