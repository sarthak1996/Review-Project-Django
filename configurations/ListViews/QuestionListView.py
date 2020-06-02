from django.views.generic import ListView
from configurations.models import Question,Choice
from configurations.FilterSets import QuestionFilter 
from collections import OrderedDict
from peer_review.HelperClasses import CommonLookups
from configurations.HelperClasses import SearchFilterBadges,SearchDropDown
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
		f_question_text=get_request.get('filter_form-question_text__icontains',None)
		f_mandatory=None if get_request.get('filter_form-mandatory',None) not in ('true','false') else get_request.get('filter_form-mandatory',None)
		f_question_choice_type=get_request.get('filter_form-question_choice_type',None)
		f_series_type=get_request.get('filter_form-series_type',None)
		f_question_type=get_request.get('filter_form-question_type',None)
		print('Generating filter tags')
		print(f_question_text,f_mandatory,f_question_choice_type,f_series_type,f_question_type)
		
		filter_badge_dict=OrderedDict({'question_text: %':f_question_text,
							'mandatory: ':f_mandatory,
							'question_choice_type: ':f_question_choice_type,
							'series_type: ':f_series_type,
							'question_type: ':f_question_type
							})
		filter_badges_list=SearchFilterBadges.generate_filter_badges_list(**filter_badge_dict)

		context['filter_badges']=filter_badges_list
		context['text_filters_drop_down_icon']=''

		context['filter']=QuestionFilter(self.request.GET,queryset=self.get_queryset(),prefix='filter_form')
		
		context['initial_filter']='Question text'
		context['other_filters']=None

		search_drop_downs_kwargs=OrderedDict({'filter_form-mandatory':[('true','Yes'),('false','No')],
									'filter_form-question_choice_type':CommonLookups.get_question_choice_types(),
									'filter_form-series_type':CommonLookups.get_series_types(),
									'filter_form-question_type':CommonLookups.get_question_types()
									})
		search_drop_downs_args=['Mandatory','Question choice type','Series type','Question type']
		#mandatory search drop down
		search_drop_downs=SearchDropDown.generate_drop_down_list(*search_drop_downs_args,**search_drop_downs_kwargs)
		context['search_drop_downs']=search_drop_downs
		context['reset_filters']='configurations:question_list_view'

		return context


