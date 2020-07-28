
function add_exemption_form(prefix){
	var form_idx = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
	$('#exemption_form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx)).on('click','a.delete_exemption_button',function(){
		return delete_exemption_form(this, 'exemption');
		});
	$('#id_'+prefix+'-TOTAL_FORMS').val(parseInt(form_idx) + 1);	
}



function delete_exemption_form(btn, prefix) {
	// console.log('Delete called')
    btn_parent=$(btn).parent()
    div_checkbox=btn_parent.children('.delete_checkbox_form')
    checkbox_input=div_checkbox.find('input')
    checkbox_input.prop('checked',true)
    btn_parent.prop('hidden',true)
    
}


function hide_deleted_exemptions(){
    div_checkbox=$('.delete_checkbox_form')
    checkbox_input=div_checkbox.find('input')
    checkbox_input.each(function(){
        if ($(this).is(':checked')){
            exemption_form=$(this).parent().parent()
            // console.log(exemption_form)
            exemption_form.prop('hidden',true)
        }
    })
}
