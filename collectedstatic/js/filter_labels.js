function remove_filter(filter_tag,prefix){
	// console.log(filter_tag)
	// console.log(prefix)
	filter_tag.prop('hidden',true);
	// call django method or modify GET request to modify the filters.
}


function hide_all_lov_filters(){
	hide_filter($('#id_filter_form-mandatory').parent().parent());
	hide_filter($('#id_filter_form-question_choice_type').parent().parent());
	hide_filter($('#id_filter_form-series_type').parent().parent());
	hide_filter($('#id_filter_form-choices').parent().parent());
	hide_filter($('#id_filter_form-question_type').parent().parent());
	hide_filter($('#id_filter_form-priority').parent().parent())
	hide_filter($('#id_filter_form-approval_outcome').parent().parent())
	hide_filter($('#id_filter_form-team').parent().parent())
	hide_filter($('#id_filter_form-review_type').parent().parent())
	hide_filter($('#id_filter_form-series_type').parent().parent())
	return;
}

function hide_filter(elem){
	elem.prop('hidden',true);
}