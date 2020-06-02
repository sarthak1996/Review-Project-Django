
from configurations.HelperClasses.DropDown import DropDown
class SearchDropDown():
	def __init__(self,title,drp_list):
		self.title=title
		self.drp_list=drp_list

	
def generate_drop_down_list(*args,**kwargs):
	print('In generate_drop_down_list')
	print(kwargs)
	print(args)
	search_drop_downs=[]
	i=0
	for (name,dropdown_values) in kwargs.items():
		lov_obj=[]
		title=args[i]
		for ind,val in enumerate(dropdown_values):
			lov_obj.append(DropDown(val[0],val[1],name))
		search_drop_downs.append(SearchDropDown(title=title,drp_list=lov_obj))
		i+=1
	print(search_drop_downs)
	return search_drop_downs

