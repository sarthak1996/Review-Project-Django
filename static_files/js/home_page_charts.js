function get_review_raised_graph(){
	var graph_comp=$('#review_raised_by_me_graph');
	$.ajax({
		url:graph_comp.data('url'),
		success:function(data){
			var ctx=graph_comp[0].getContext('2d');
			console.log('Generating chart');
			console.log(ctx);
			console.log(data);
			// Chart.defaults.global.defaultFontSize=16;
			new Chart(ctx,{
				type:'line',
				data:{
					labels:data.labels,
					datasets:[{
								label:'Raised by Me',
								 backgroundColor: 'rgba(100,255,218, 0.3)',
								 borderColor: 'rgba(100,255,218, 0.8)',
								data:data.data1
							},
							{
								label:'Raised to Me',
								backgroundColor: 'rgba(118,255,3, 0.3)',
								 borderColor: 'rgba(118,255,3, 0.8)',
								data:data.data2
							}
					],
				},
				options:{
					responsive:true,
					title:{
						display:true,
						text:'Mergereq checklist',
						fontSize:20
					},
					scales: {
						xAxes: [{
				            gridLines: {
				                 drawOnChartArea: false
				            }
				        }],
            			yAxes: [{
                			ticks: {
                    		beginAtZero: true
                			},
                			gridLines: {
                				 drawOnChartArea: false
            				}   
                			// stacked:true
            			}]
        			}
				}
		});
		}
	});
}




function get_peer_testing_graph(){
	var graph_comp=$('#peer_testing_graph');
	$.ajax({
		url:graph_comp.data('url'),
		success:function(data){
			var ctx=graph_comp[0].getContext('2d');
			console.log('Generating chart');
			console.log(ctx);
			console.log(data);
			// Chart.defaults.global.defaultFontSize=16;
			new Chart(ctx,{
				type:'line',
				data:{
					labels:data.labels,
					datasets:[{
								label:'Raised by Me',
								 backgroundColor: 'rgba(100,255,218, 0.3)',
								 borderColor: 'rgba(100,255,218, 0.8)',
								data:data.data1
							},
							{
								label:'Raised to Me',
								backgroundColor: 'rgba(118,255,3, 0.3)',
								 borderColor: 'rgba(118,255,3, 0.8)',
								data:data.data2
							}
					],
				},
				options:{
					responsive:true,
					title:{
						display:true,
						text:'Peer Testing',
						fontSize:20
					},
					scales: {
						xAxes: [{
				            gridLines: {
				                 drawOnChartArea: false
				            }
				        }],
            			yAxes: [{
                			ticks: {
                    		beginAtZero: true
                			},
                			gridLines: {
                				 drawOnChartArea: false
            				}   
                			// stacked:true
            			}]
        			}
				}
		});
		}
	});
}