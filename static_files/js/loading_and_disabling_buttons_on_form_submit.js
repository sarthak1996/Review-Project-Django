function load_and_disable_button_form_submit(){
	$('.btn').attr('disabled',true);
	$('.btn').html("<i class=\"fa fa-spinner fa-spin\"></i>");
	return true;
}