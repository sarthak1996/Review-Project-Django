from django.forms import BaseModelFormSet
class RequiredFormSet(BaseModelFormSet):
	def __init__(self, *args, **kwargs):
		super(RequiredFormSet, self).__init__(*args, **kwargs)
		print('setting empty_permitted to false')
		for form in self.forms:
			form.empty_permitted = False