import logging

class SystemLogFilter(logging.Filter):
	def filter(self, record):
		return True
