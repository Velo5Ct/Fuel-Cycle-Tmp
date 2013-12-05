function doGraph(responseObj,ctx){


				//alert("Generating figure");

				//Chart data
				var lwry = responseObj.LWRy;
				var fry = responseObj.FRy;
				var moxy = responseObj.MOXy;

				var lwrx = responseObj.LWRx;
				var frx = responseObj.FRx;
				var moxx = responseObj.MOXx;


			
				var graphdata = {
					labels: lwrx,
					datasets: [
					    {
						fillColor: "rgba(151,187,205,0.5)",
						strokeColor : "rgba(151,187,205,1)",
						//pointColor : "rgba(151,187,205,1)",
						data: lwry
					    },
					    {
						fillColor: "rgba(187,157,202,0.2)",
						strokeColor : "rgba(101,117,105,1)",
						//pointColor : "rgba(151,187,205,1)",
						data: fry
					    },
					    {
						fillColor: "rgba(247,251,22,0.6)",
						strokeColor : "rgba(201,11,105,1)",
						data: moxy
					    }
					]
				};
				options={
					scaleLineColor : "rgba(0,0,0,.1))",
					scaleFontSize:8,
					scaleLineWidth: 1,
					scaleShowLabels: true,
					scaleLabel: "<%=value%>",
					scaleFontColor: "#666",
					scaleShowGridLines: true,
					pointDot: false
					};
				new Chart(ctx).Line(graphdata,options);


}






/*------UI Functions-----------*/

$(function(){

	//Chart
	var c=$('#fchart1').get(0);
	var ctx = c.getContext('2d');





	$("#tabbedContent").load("determ.htm");
	$("#tabs").tabs({active:0 });



	$("#loadDeterm").click(function(){

		var activetab= $("#tabs").tabs("option","active");
		sessionStorage.setItem("activetab",activetab);

		$("li.ld2").removeClass('active');
		$("li.ld1").addClass('active');

		$("#tabbedContent").load('determ.htm');
		
	});
	
	$("#loadStochast").click(function(){
		
		var activetab= $("#tabs").tabs("option","active");
		sessionStorage.setItem("activetab",activetab);

		$("li.ld1").removeClass('active');
		$("li.ld2").addClass('active');


		$("#tabbedContent").load('stochast.htm');



		
	});


	//=================  Form Input Validation ==================
	
	$('#fcsubmit').ajaxForm({
		
		success: function(responseObj, statusText, xhr, $form){ 
		
				window.scrollTo(10,10);


				var modelType = responseObj.modelType;

				if (modelType == 's'){
					
					$("#ResultPane").hide();

					//Generate graph
					doGraph(responseObj,ctx);

					$("#GraphPane").slideDown(1000);
						
					
					var nrealizations = responseObj.nrealizations;
					$("#Realizations").html("Num Realizations: " + nrealizations ); 
					
				}else{
					$("#GraphPane").hide();

					var lwr = responseObj.LWR;
					var fr =  responseObj.FR;
					var mox = responseObj.MOX;
				

					$("#mainValue").html("LWR:" + lwr + " $mil/Kwh");
					$("#underValue").html("FR:" + fr + "&nbsp;&nbsp;MOX:" + mox);

					$("#ResultPane").slideDown(1000);
				}

		},

		dataType:'json',
		url: 'fcycle.py',
		timeout: 5000	
		
		
	}); 
});
