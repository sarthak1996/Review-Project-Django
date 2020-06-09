def is_manager(user):
	if user:
		print('Permission resolving as manager returned :'+str(user.groups.filter(name='Manager').count()>0))
		return user.groups.filter(name='Manager').count()>0
	return False

def is_employee(user):
	if user:
		print('Permission resolving as manager returned :'+str(user.groups.filter(name='Employee').count()>0))
		return user.groups.filter(name='Employee').count()>0
	return False

def is_emp_or_manager(user):
	return is_employee(user) or is_manager(user)