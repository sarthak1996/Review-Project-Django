from django.forms import BaseModelFormSet
from configurations.HelperClasses import LoggingHelper
import traceback
class RequiredFormSet(BaseModelFormSet):
	def __init__(self, *args, **kwargs):
		super(RequiredFormSet, self).__init__(*args, **kwargs)
		logger=LoggingHelper(self.request.user,__name__)
		logger.write('setting empty_permitted to false',LoggingHelper.DEBUG)
		for form in self.forms:
			form.empty_permitted = False