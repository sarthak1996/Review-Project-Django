from django.forms import ModelForm
from configurations.models import Question,Series,Choice
from django import forms
from configurations.HelperClasses import CustomMultiSelectCheckbox

class QuestionForm(ModelForm):
	question_text=forms.CharField(label='Question Text',required=True,widget=forms.TextInput(attrs={'placeholder': 'Question Text','class':'form-control'}))
	question_choice_type=forms.ChoiceField(required=True,choices=Question.get_questions_choice_types()['question_choice_type'],widget=forms.Select(attrs={'class':'form-control choice_select','label':'Question choice type'}))
	mandatory=forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'label':'Mandatory','class':'form-check-input choice_check_box_select'}))
	series_type=forms.ChoiceField(required=False,choices=Series.get_choices_models()['series_type'],widget=forms.Select(attrs={'class':'form-control choice_select','label':'Series type'}))
	question_type=forms.ChoiceField(required=True,choices=Question.get_questions_choice_types()['question_type'],widget=forms.Select(attrs={'class':'form-control choice_select','label':'Question type'}))
	choices=forms.ModelMultipleChoiceField(required=False,queryset=Choice.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'class':'no_bullets choice_check_box_multi_select','label':'Choices'}))
	#attrs={'label':'Choices','class':'form-check-input choice_check_box_multi_select'})
	class Meta:
		model=Question
		fields=['question_text','question_choice_type','mandatory','series_type','question_type','choices']