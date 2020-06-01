def generate_filter_badges_list(**kwargs):
	filter_badges_list=[]
	print('In generate filter badges list')
	print(kwargs)
	for (key,val) in kwargs.items():
		if val:
			filter_badges_list.append(key+val+('%' if key[-1]=='%' else ''))
	print(filter_badges_list)
	return filter_badges_list