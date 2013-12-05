
function sdiff(strA, strB){
	return parseFloat(strA) - parseFloat(strB);
}


$(function(){


	$(".reg_input").change(function(){
		
		var slidername = "#" + $(this).attr('id') + "slider";
		$(slidername).slider("value", $(this).val());
		
	});

	$(".mu_input").change(function(){
		
		var slidername = "#" + $(this).attr('id') + "slider";
		var stdname = "#" + $(this).attr('id') + "std";
		var newstdval =  parseFloat($(slidername).slider('values',1)) - parseFloat($(this).val());
		$(slidername).slider("values", [ $(this).val(), $(slidername).slider('values',1)  ]   );
		$(stdname).val(newstdval);
		
	});

	$(".std_input").change(function(){
		var stdn = $(this).attr('id');
		
		var slidername = "#" + stdn.substr(0, (stdn.length - 'std'.length)) + 'slider';
		var mu = parseFloat($(slidername).slider("values",0));
		var stdval  = parseFloat($(this).val()) + mu;
		$(slidername).slider("values", [ mu , stdval ]   );
		
	});



	$("#nrealizeslider").slider({
		min:1,
		animate:true,
		max:10000,
		steps:1,
		range:false,
		value:500,
		slide: function(event,ui){
			$("#nrealize").val(ui.value);
		}
			
	});
	$("#nrealize").val($("#nrealizeslider").slider("value"));


	$("#irslider").slider({
		
		range:true,
		min:0,
		max:1,
		step:0.001,
		values: [0.1,0.117],
		slide: function(event,ui){
			$("#ir").val(ui.values[0]);
			$("#irstd").val(ui.values[1] -ui.values[0]);
		}
		
		});



	$("#cc1slider").slider({
		
		range:true,
		min:0,
		max:3000,
		step:100,
		values: [1800,2300],
		slide: function(event,ui){
			$("#cc1").val(ui.values[0]);
			$("#cc1std").val(ui.values[1]- ui.values[0]);
		}
		
	});

	$("#com1slider").slider({
		
		range:true,
		min:0,
		max:100,
		step:1.0,
		values: [78,78 + 7.8],
		slide: function(event,ui){
			$("#com1").val(ui.values[0]);
			$("#com1std").val(ui.values[1]- ui.values[0]);
		}
		
	});

	$("#c1slider").slider({
		
		range:true,
		min:5,
		max:600,
		step:1,
		values: [100,100+17],
		slide: function(event,ui){
			$("#c1").val(ui.values[0]);
			$("#c1std").val(ui.values[1]- ui.values[0]);
		}
		
	});

	$("#c2slider").slider({
		
		range:true,
		min:5,
		max:20,
		step:0.1,
		values: [11.5,11.5+1.7],
		slide: function(event,ui){
			$("#c2").val(ui.values[0]);
			$("#c2std").val(ui.values[1]- ui.values[0]);
		}
		
	});

	$("#c3slider").slider({
		
		range:true,
		min:50,
		max:200,
		step:0.1,
		values: [115,115+5.1],
		slide: function(event,ui){
			$("#c3").val(ui.values[0]);
			$("#c3std").val(ui.values[1]- ui.values[0]);
		}
		
	});

	$("#c4slider").slider({
		
		range:true,
		min:100,
		max:500,
		step:0.1,
		values: [220,220+9.2],
		slide: function(event,ui){
			$("#c4").val(ui.values[0]);
			$("#c4std").val(ui.values[1]- ui.values[0]);
		}
		
	});


	$("#c5slider").slider({
		
		range:true,
		min:0,
		max:500,
		step:0.1,
		values: [0,0],
		slide: function(event,ui){
			$("#c5").val(ui.values[0]);
			$("#c5std").val(ui.values[1]- ui.values[0]);
		}
		
	});



	$("#cwlslider").slider({
		
		range:true,
		min:0,
		max:2,
		step:0.01,
		values: [1,1],
		slide: function(event,ui){
			$("#cwl").val(ui.values[0]);
			$("#cwlstd").val(ui.values[1]- ui.values[0]);
		}
		
	});




	$("#cfpcondslider").slider({
		
		range:true,
		min:1000,
		max:11000,
		step:10,
		values: [5400,5400+1502],
		slide: function(event,ui){
			$("#cfpcond").val(ui.values[0]);
			$("#cfpcondstd").val(ui.values[1]- ui.values[0]);
		}
		
	});






	$("#tconsslider").slider({
		
		range:true,
		min:0,
		max:20,
		step:0.1,
		values: [7,7+0.7],
		slide: function(event,ui){
			$("#tcons").val(ui.values[0]);
			$("#tconsstd").val(ui.values[1]- ui.values[0]);
		}
		
	});





	$("#teconsslider").slider({
		
		range:true,
		min:0,
		max:50,
		step:0.5,
		values: [30,30+3],
		slide: function(event,ui){
			$("#tecons").val(ui.values[0]);
			$("#teconsstd").val(ui.values[1]- ui.values[0]);
		}
		
	});


	
	$("#csslider").slider({
		range:true,
		min:0,
		max:2000,
		step:1,
		values:[502,502+63],
		slide:function(event,ui){
			$("#cs").val(ui.values[0]);
			$("#csstd").val(ui.values[1]-ui.values[0]);
		}
	});





	$("#com2slider").slider({
		range:true,
		min:10,
		max:200,
		step:1,
		values:[70,70+7],
		slide:function(event,ui){
			$("#com2").val(ui.values[0]);
			$("#com2std").val(ui.values[1]-ui.values[0]);
		}
	});




	$("#cc2slider").slider({
		range:true,
		min:1000,
		max:3000,
		step:1,
		values:[2000,2000+410],
		slide:function(event,ui){
			$("#cc2").val(ui.values[0]);
			$("#cc2std").val(ui.values[1]-ui.values[0]);
		}
	});




	$("#rbslider").slider({
		range:true,
		min:0,
		max:1000,
		step:1,
		values:[211,211+35],
		slide:function(event,ui){
			$("#rb").val(ui.values[0]);
			$("#rbstd").val(ui.values[1]-ui.values[0]);
		}
	});




	$("#fr1slider").slider({
		range:true,
		min:500,
		max:5000,
		step:1,
		values:[2700,2700+552],
		slide:function(event,ui){
			$("#fr1").val(ui.values[0]);
			$("#fr1std").val(ui.values[1]-ui.values[0]);
		}
	});




	$("#ff1slider").slider({
		range:true,
		min:500,
		max:3500,
		step:1,
		values:[1800,1800+180],
		slide:function(event,ui){
			$("#ff1").val(ui.values[0]);
			$("#ff1std").val(ui.values[1]-ui.values[0]);
		}
	});

	


	$("#cb1slider").slider({
		range:true,
		min:1000,
		max:3000,
		step:1,
		values:[1600,1600+751],
		slide:function(event,ui){
			$("#cb1").val(ui.values[0]);
			$("#cb1std").val(ui.values[1]-ui.values[0]);
		}
	});




});

