import django_filters
from configurations.models import Question
class QuestionFilter(django_filters.FilterSet):
	class Meta:
		model=Question
		fields=('question_text','question_choice_type','mandatory','series_type','choices','question_type')
