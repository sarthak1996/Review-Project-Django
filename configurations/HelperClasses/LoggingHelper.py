import logging
import logging.handlers as handlers
class LoggingHelper():
	
	DEBUG=10
	INFO=20
	WARNING=30
	ERROR=40

	def __init__(self,user,name):
		self.user=user
		self.name=name
	
	def write(self,log_text,logging_level):
		self.__resolve_logger_level_and_log(log_text,logging_level)

	def __resolve_logger_level_and_log(self,log_text,logging_level):
		uname=None
		if getattr(self,'user',None) and self.user and self.user.username:
			uname=self.user.username
		if log_text:
			log_text=log_text.replace('%','%%')
			log_text='( User: ' + str(uname) + ' ) => ' + log_text
		logging.basicConfig()
		logger = logging.getLogger()
		
		if logging_level==LoggingHelper.DEBUG:
			logger.debug(log_text)
		elif logging_level==LoggingHelper.INFO:
			logger.info(log_text)
		elif logging_level==LoggingHelper.WARNING:
			logger.warning(log_text)
		elif logging_level==LoggingHelper.ERROR:
			logger.error(log_text)

