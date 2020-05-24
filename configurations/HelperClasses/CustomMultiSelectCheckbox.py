from django.forms import widgets
class CustomMultiSelectCheckbox(widgets.CheckboxSelectMultiple):
	def render(self, *args, **kwargs):
		output = super(CheckboxSelectMultiple, self).render(*args,**kwargs)
		output=mark_safe(output.replace(u'<ul>', u'<ul class="checkbox-select">'))
		return output