
from configurations.HelperClasses.DropDown import DropDown
from configurations.HelperClasses import LoggingHelper

class SearchDropDown():
	def __init__(self,title,drp_list):
		self.title=title
		self.drp_list=drp_list

	
def generate_drop_down_list(request,*args,**kwargs):
	logger=LoggingHelper(request.user,__name__)
	logger.write('In generate_drop_down_list',LoggingHelper.DEBUG)
	logger.write('args:'+str(args),LoggingHelper.DEBUG)
	logger.write('kwargs:'+str(kwargs),LoggingHelper.DEBUG)

	search_drop_downs=[]
	i=0
	for (name,dropdown_values) in kwargs.items():
		lov_obj=[]
		title=args[i]
		for ind,val in enumerate(dropdown_values):
			lov_obj.append(DropDown(val[0],val[1],name))
		search_drop_downs.append(SearchDropDown(title=title,drp_list=lov_obj))
		i+=1
	logger.write('search_drop_downs:'+str(search_drop_downs),LoggingHelper.DEBUG)
	return search_drop_downs

