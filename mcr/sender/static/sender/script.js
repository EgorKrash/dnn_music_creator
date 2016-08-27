//    variables 
music_playing = false;
wait_status = true;
audio = document.createElement('audio');
pause_time = 0;
sound_on = true;
//a = Math.floor(Math.random()*1000);
a = 1;


// functions
function music_play() {
		if (wait_status == false) {
			audio.play(pause_time);
			music_playing = true;
			$('#play_triangle').animate({opacity: 0}, 200, function(){});
			$('#pause_sticks').animate({opacity: 1}, 200, function(){});
			$('#wait').animate({opacity: 0}, 200, function(){});
		}};

function music_pause() {
	pause_time = audio.currentTime
	audio.pause();
	music_playing = false;
	$('#pause_sticks').animate({opacity: 0}, 200, function(){});
	$('#play_triangle').animate({opacity: 1}, 200, function(){})};

function wait() {
	$('#pause_sticks').animate({opacity: 0}, 200, function(){});
	$('#play_triangle').animate({opacity: 0}, 200, function(){});
	$('#wait').animate({opacity: 1}, 200, function(){});
	
}

function get_song(a) {
	wait_status = true;
	function success(json){
		if (json.status == 'OK') {
			wait_status = false;
			audio.src = '/static/music/' + a + '.mp3';
			music_play(a);

			console.log('music ready');
		} else {
			setTimeout(function(){get_song(a)}, 6000);
			wait_status = true;
			wait();
			console.log(json);

		}
	}
	jQuery.get('/sender/api/music/', {'a': a}, success, 'json').fail(
		function() {setTimeout(function(){console.log('get'); get_song(a)}, 5000)});}


$(window).load(function(){
	get_song(a);
	
	$('#player_circle').click(function(){
		if (music_playing == false) {music_play(a)} else {music_pause()}
	})

//     hover animation	
	$('#player').hover(function(){
		$('#reset').animate({left: '-22em', opacity: 1}, 300, function(){});
		$('#sound').animate({left: '18.7em', opacity: 1}, 300, function(){});
		$('#player').animate({opacity: 1}, 200, function(){})}, function(){
		$('#player_circle').css('box-shadow', '0 0 0 0');
		$('#reset').animate({left: '0em', opacity: 0}, 200, function(){});
		$('#sound').animate({left: '9em', opacity: 0}, 200, function(){});
		$('#player').animate({opacity: 0.8}, 200, function(){});})

	$("#sound").hover(function(){
		$("#dinamic").animate({opacity: 1}, 100, function(){});}, function(){
		$("#dinamic").animate({opacity: 0.8}, 100, function(){});});

	$("#reset").hover(function(){
		$("#reset_circle").animate({opacity: 1}, 100, function(){});}, function(){
		$("#reset_circle").animate({opacity: 0.8}, 100, function(){});});
	
	$("#sound").click(function(){
		if (sound_on == true) {
			$("#mute_x").animate({opacity: 1}, 100, function(){});
			audio.volume = 0;
			sound_on = false;
		}
		else {
			$("#mute_x").animate({opacity: 0}, 100, function(){});
			sound_on = true;
			audio.volume = 1;
		}})

	$("#reset").click(function(){
		if (wait_status == false) {
			audio.pause();
			audio.src = '';
			a = Math.floor(Math.random()*1000);
			get_song(a);
			console.log(a);
		}})	

	$("#reset").rotate({bind:{click: function(){
		$(this).rotate({
			angle: 0,
			animateTo:360}
			)}}});
})	