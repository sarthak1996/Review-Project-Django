function refresh_choices_region(url,choice_type){
	// console.log('Js')
	// console.log(url)
	// console.log(team_id)
	$.ajax({                       
        url: url,                    
        data: {
          'choice_type': choice_type       
        },
        success: function (data) {   
          $("#id_choices").html(data);  
        }
      });
}