from django.forms import ModelForm
from django import forms
from peer_review.models import Review
from django.contrib.auth import get_user_model
from peer_testing.models import Answer
from configurations.models import Choice,Question
from concurrency.forms import VersionWidget
class PeerReviewAnswerForm(ModelForm):

	single_choice_field=forms.ModelChoiceField(required=False,queryset=Choice.objects.all(),empty_label='Choose a value',widget=forms.Select(attrs={'class':'form-control not_rendered choice_select'}))
	text_answer = forms.CharField(required=False,label='Answer Text',widget=forms.Textarea(attrs={'placeholder': 'Answer Text','class':'form-control text_area not_rendered'}))
	question=forms.ModelChoiceField(required=False,queryset=Question.objects.all(),empty_label="Choose a Question",widget=forms.Select(attrs={'class':'form-control choice_select not_rendered'}))
	version=VersionWidget(attrs={'placeholder': 'Object version number','class':'form-control version_widget'})
	class Meta:
		model=Answer
		fields=['question','version']

	def __init__(self, *args, **kwargs):
		super(PeerReviewAnswerForm, self).__init__(*args, **kwargs)
		if 'question' in self.initial :
			selected_question=self.initial['question']
			self.fields['question'].value =selected_question
			self.fields['text_answer'].label=selected_question.question_text
			question_choices=Question.get_questions_choice_types()['question_choice_type']
			answer_type=self.fields['text_answer']
			if selected_question.question_choice_type == question_choices[0][0]:
				answer_type=self.fields['single_choice_field']
				answer_type.queryset=selected_question.choices.all()
			elif selected_question.question_choice_type == question_choices[2][0]:
				answer_type=self.fields['text_answer']

			answer_type.label=selected_question.question_text
					
			if selected_question.mandatory:
				answer_type.required=True
			answer_type.widget.attrs['class']=answer_type.widget.attrs['class'].replace('not_rendered','')

