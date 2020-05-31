from django.views.generic import ListView
from configurations.models import Question
from configurations.FilterSets import QuestionFilter 
from collections import OrderedDict
from peer_review.HelperClasses import CommonLookups
class QuestionListView(ListView):
	model=Question
	template_name='configurations/list_view.html'


	def get_context_data(self,**kwargs):
		# print('Helo')
		context = super().get_context_data(**kwargs)
		context['create_url']='configurations:question_create_view'
		context['create_object_button_title']='Create Question'
		context['detail_view_url']='configurations:question_detail_view'
		context['page_title']='Question'
		context['create_button_rendered']=True
		number_badges_dict=OrderedDict()
		number_badges_dict['Peer Review']=Question.objects.filter(question_type=CommonLookups.get_peer_review_question_type()).all().count()
		number_badges_dict['Peer Testing']=Question.objects.filter(question_type=CommonLookups.get_peer_testing_question_type()).all().count()
		context['read_only_number_badges']=number_badges_dict.items()
		# print('Filter request')
		# print(self.request.GET)

		#filter badges initialization
		get_request=self.request.GET
		f_question_text=get_request.get('filter_form-question_text',None)
		f_mandatory='' if get_request.get('filter_form-mandatory',None) not in (True,False) else get_request.get('filter_form-mandatory',None)
		f_question_choice_type=get_request.get('filter_form-question_choice_type',None)
		f_series_type=get_request.get('filter_form-series_type',None)
		f_question_type=get_request.get('filter_form-question_type',None)
		print('Generating filter tags')
		print(f_question_text,f_mandatory,f_question_choice_type,f_series_type,f_question_type)
		
		filter_badges_list=self.generate_filter_list(text=f_question_text,
													mandatory=f_mandatory,
													choice=f_question_choice_type,
													series=f_series_type,
													q_type=f_question_type)
		context['filter_badges']=filter_badges_list

		context['filter']=QuestionFilter(self.request.GET,queryset=self.get_queryset(),prefix='filter_form')
		return context

	def generate_filter_list(self,text,mandatory,choice,series,q_type):
		filter_badges_list=[]
		if text :
			filter_badges_list.append('question_text: %'+text+'%')
		if mandatory:
			filter_badges_list.append('mandatory: '+mandatory)
		if choice:
			filter_badges_list.append('question_choice_type: '+choice)
		if series:
			filter_badges_list.append('series_type: '+series)
		if q_type:
			filter_badges_list.append('question_type: '+q_type)
		return filter_badges_list


