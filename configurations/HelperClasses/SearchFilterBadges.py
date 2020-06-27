from configurations.HelperClasses import LoggingHelper

def generate_filter_badges_list(request,**kwargs):
	filter_badges_list=[]
	logger=LoggingHelper(request.user,__name__)
	logger.write('In generate filter badges list',LoggingHelper.DEBUG)
	logger.write('kwargs:'+str(kwargs),LoggingHelper.DEBUG)
	for (key,val) in kwargs.items():
		if val:
			filter_badges_list.append(key+val+('%' if key[-1]=='%' else ''))
	logger.write('filter_badges_list:'+str(filter_badges_list),LoggingHelper.DEBUG)
	return filter_badges_list