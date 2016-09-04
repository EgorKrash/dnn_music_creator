$(window).load(function() {
	
	var menu_open = false;
	$('#menu_btn').click(function() {
		if (menu_open === false) {
			$('#menu').animate({
				opacity: 1
			}, 400, function() {});
			menu_open = true;
		} else {
			$('#menu').animate({
				opacity: 0
			}, 400, function() {});
			menu_open = false;
		}
	});

	$('#menu_btn').hover(function(){
		$('#menu_btn_shape').animate({
			opacity:1
		}, 200, function(){})
	}, function(){
		$('#menu_btn_shape').animate({
			opacity:0.5
		}, 200, function(){})
	});

	$('.menu_link').hover(function(){
		$(this).animate({
			opacity: 1
		}, 200, function(){})
	}, function(){
		$(this).animate({
			opacity: 0.7
		}, 200, function(){})
	})

})