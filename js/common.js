$(function(){

	var activetab = sessionStorage.getItem("activetab");
	$("#tabs").tabs({active:activetab});


	


	/*   Set default  Values*/
	$("#bu1").prop("selectedIndex", 1);
	$("#bu3").prop("selectedIndex", 1);




	//Ensure Bu3 >= Bu1
	$("#bu1").change(function(){
		
		var sl = $(this).prop('selectedIndex');
		var bu3sl = $("#bu3").prop("selectedIndex");

		
		switch(sl)
		{
			case 0:
				$("#bu3 option:eq(0)").prop('disabled',false);	
				$("#bu3 option:eq(1)").prop('disabled',false);	
				$("#bu3 option:eq(2)").prop('disabled',false);	
			break;
			case 1:
				//remove option 1 if previously added
				$("#bu3 option:eq(1)").prop('disabled',false);	
				$("#bu3 option:eq(2)").prop('disabled',false);	
				$("#bu3 option:eq(0)").prop('disabled',true);	
				if( bu3sl == 0)
					$("#bu3").val( $("#bu3 option:eq(1)").val());
				
			break;
			case 2:
				//only option 2 is valid
				$("#bu3 option:eq(0)").prop('disabled',true);	
				$("#bu3 option:eq(1)").prop('enabled',true);	
				$("#bu3 option:eq(2)").prop('disabled',true);	
				if( bu3sl == 0 || bu3sl == 2){
					$("#bu3").val( $("#bu3 option:eq(1)").val());
				}
			break;

		}

	});

});


