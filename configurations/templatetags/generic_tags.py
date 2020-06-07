from django import template

register = template.Library()
class EnumeratedDictionaryObject():
	def __init__(self,key,value,index):
		self.key=key
		self.value=value
		self.index=index

@register.simple_tag(takes_context=True)
def enumerate_objects(context,objects):
	return_obj=[]
	i=0
	for key,val in objects:
		return_obj.append(EnumeratedDictionaryObject(key=key,
													value=val,
													index=i))
		i+=1
	return return_obj