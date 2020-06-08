class Timeline():
	def __init__(self,title,description,timeline_url=None,is_url=False,obj_pk=None,title_right_floater=None):
		self.title=title
		self.timeline_url=timeline_url
		self.description=description
		self.is_url=is_url
		self.obj_pk=obj_pk
		self.title_right_floater=title_right_floater
	def __str__(self):
		return self.title + ' : ' + '\n\t-'.join([desc for desc in self.description]) + '=>' + str(self.is_url)