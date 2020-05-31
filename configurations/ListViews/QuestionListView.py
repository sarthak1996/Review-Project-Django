from django.views.generic import ListView
from configurations.models import Question,Choice
from configurations.FilterSets import QuestionFilter 
from collections import OrderedDict
from peer_review.HelperClasses import CommonLookups
from configurations.HelperClasses.SearchDropDown import SearchDropDown
from configurations.HelperClasses.DropDown import DropDown
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
		# number_badges_dict=OrderedDict()
		# number_badges_dict['Peer Review']=Question.objects.filter(question_type=CommonLookups.get_peer_review_question_type()).all().count()
		# number_badges_dict['Peer Testing']=Question.objects.filter(question_type=CommonLookups.get_peer_testing_question_type()).all().count()
		# context['read_only_number_badges']=number_badges_dict.items()

		# print('Filter request')
		# print(self.request.GET)

		#filter badges initialization
		get_request=self.request.GET
		f_question_text=get_request.get('filter_form-question_text',None)
		f_mandatory=None if get_request.get('filter_form-mandatory',None) not in ('true','false') else get_request.get('filter_form-mandatory',None)
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
		context['initial_filter']='Question text'
		context['other_filters']=None

		search_drop_downs=[]

		#mandatory search drop down
		lov_obj=[]
		for i,elem in enumerate([('true','Yes'),('false','No')]):
			lov_obj.append(DropDown(elem[0],elem[1],'filter_form-mandatory'))
		mandatory_drp_list=lov_obj
		mandatory_drp=SearchDropDown(title='Mandatory',drp_list=mandatory_drp_list)
		#choice type search drop down
		lov_obj=[]
		for i,elem in enumerate(CommonLookups.get_question_choice_types()):
			lov_obj.append(DropDown(elem[0],elem[1],'filter_form-question_choice_type'))
		
		choice_type_drp_list=lov_obj
		choice_type_drp=SearchDropDown(title='Question choice type',drp_list=choice_type_drp_list)
		#series type
		lov_obj=[]
		for i,elem in enumerate(CommonLookups.get_series_types()):
			lov_obj.append(DropDown(elem[0],elem[1],'filter_form-series_type'))
		series_type_drp_list=lov_obj
		series_type_drp=SearchDropDown(title='Series type',drp_list=series_type_drp_list)
		#question type
		lov_obj=[]
		for i,elem in enumerate(CommonLookups.get_question_types()):
			lov_obj.append(DropDown(elem[0],elem[1],'filter_form-question_type'))
		q_type_drp_list=lov_obj
		q_type_drp=SearchDropDown(title='Question type',drp_list=q_type_drp_list)
		
		search_drop_downs.append(mandatory_drp)
		search_drop_downs.append(choice_type_drp)
		search_drop_downs.append(series_type_drp)
		search_drop_downs.append(q_type_drp)
		context['search_drop_downs']=search_drop_downs
		context['reset_filters']='configurations:question_list_view'

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


