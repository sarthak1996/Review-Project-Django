from peer_review.HelperClasses import CommonLookups
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def get_page_obj(filter,request):
	paginator=Paginator(filter.qs,CommonLookups.get_pagination_value())
	page = request.get('page')
	response_objs=None
	try:
		response_objs = paginator.page(page)
	except PageNotAnInteger:
		response_objs = paginator.page(1)
	except EmptyPage:
		response_objs = paginator.page(min(1,paginator.num_pages))
	return response_objs

def get_applied_filters_url(filter_dict):
	url=''
	for i in filter_dict:
		if filter_dict[i]:
			url+='&'+i+'='+filter_dict[i]
	return url