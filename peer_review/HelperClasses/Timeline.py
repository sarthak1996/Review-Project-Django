from configurations.HelperClasses import LoggingHelper
import traceback
class Timeline():
	def __init__(self,title,description,request,timeline_url=None,is_url=False,obj_pk=None,title_right_floater=None):
		self.title=title
		self.timeline_url=timeline_url
		self.description=description
		self.is_url=is_url
		self.obj_pk=obj_pk
		self.title_right_floater=title_right_floater
		self.request=request

	def __str__(self):
		logger=LoggingHelper(self.request.user,__name__)
		logger.write('Description',LoggingHelper.DEBUG)
		logger.write(str(self.description),LoggingHelper.DEBUG)
		desc_str='\n\t-'.join([desc for desc in self.description]) if self.description else '***Description None***'
		logger.write(str(desc_str),LoggingHelper.DEBUG)
		return self.title + ' : ' + desc_str + '=>' + str(self.is_url)