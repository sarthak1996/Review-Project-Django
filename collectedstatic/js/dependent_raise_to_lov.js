function refresh_raise_to_lov(url,team_id){
	// console.log('Js')
	// console.log(url)
	// console.log(team_id)
	$.ajax({                       
        url: url,                    
        data: {
          'team': team_id       
        },
        success: function (data) {   
          $("#id_raise_to").html(data);  
        }
      });
}