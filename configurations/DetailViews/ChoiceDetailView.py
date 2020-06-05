from django.views.generic.detail import DetailView
from configurations.models import Choice,Question
from peer_review.HelperClasses import Timeline
class ChoiceDetailView(DetailView):
	model=Choice
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'

	def get_context_data(self, **kwargs):
		context=super(ChoiceDetailView,self).get_context_data(**kwargs)
		choice_obj=self.object
		context['detail_view_card_title']='Choice'
		context['detail_name']=choice_obj.choice_text
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Choice'
		context['update_view_url']='configurations:choice_update_view'
		context['button_label']='Update'
		context['update_rendered']=True
		context['delegate_rendered']=False
		context['delegate_label']='Delegate'
		context['delegate_view_url']='peer_review:delegate_view'

		choice_questions=Question.objects.filter(choices=choice_obj)
		question_url='configurations:question_detail_view'
		choice_usages=[]
		for question in choice_questions:
			choice_usages.append(Timeline(title=question.question_text,
											timeline_url=question_url,
											description=question.question_type,
											is_url=True,
											obj_pk=question.pk
											))
		print('\n'.join([str(usage) for usage in choice_usages]))
		context['right_aligned_timeline_title']='Question Usages'
		context['right_aligned_timeline']=choice_usages



		return context