function keep_initial_filter_as_displayed(){
	$('.filter_hidden').parent().parent().prop('hidden',true);
}

function on_select_filter_change(btn){
	id_value=$(btn).attr("data-search-id");
	$(btn).parent().parent().parent().parent().parent().prop('hidden',true);
	console.log($(btn))
	console.log($(id_value))
	form_element=$('#id_'+id_value);
	console.log($(form_element))
	console.log($(form_element).parent().parent())
	$(form_element).parent().parent().prop('hidden',false);
}