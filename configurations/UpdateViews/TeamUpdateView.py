from django.views.generic.edit import UpdateView 
from configurations.models import Team
from configurations.forms.TeamForm import TeamForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from configurations.Exceptions import OptimisticLockingException
from django.urls import reverse_lazy
from django.db import transaction

class TeamUpdateView(UpdateView):
	model=Team
	template_name='configurations/create_view.html'
	# fields=[
	# 	'team_name',
	# 	'team_grp_mail',
	# ]
	form_class=TeamForm
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	@transaction.atomic
	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		try :
			redirect = super().form_valid(form)
		except OptimisticLockingException as e:
			form.add_error(None,'Some user has updated this object while you were trying to do the same. Please open the object again and update')
			return super(TeamUpdateView,self).form_invalid(form)
		except Exception as e:
			form.add_error(None,str(e))
			return super(TeamUpdateView,self).form_invalid(form)
		messages.success(self.request, 'Successfully updated team : '+form.instance.team_name)
		return redirect

	def get_context_data(self, **kwargs):
		context=super(TeamUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Team'
		context['card_title']='Team'
		context['is_conf_active']='active'
		return context


	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(TeamUpdateView, self).dispatch(*args, **kwargs)


	def get_object(self,queryset=None):
		obj=getattr(self,'object',None)
		if not obj:
			if queryset is None:
				queryset = self.get_queryset()
			pk = self.kwargs.get(self.pk_url_kwarg, None)
			if pk is not None:
				queryset = queryset.filter(pk=pk)
			try:
			    # Get the single item from the filtered queryset
				print(self)
				obj = queryset.get()
				print('Picking cached object')
				print(obj.version)
			except ObjectDoesNotExist:
				raise Http404(_("No %(verbose_name)s found matching the query") %
		                  {'verbose_name': queryset.model._meta.verbose_name})
		return obj


		