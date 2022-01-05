
// var isAudioPlaying = "false";
// var startAudio = document.getElementById("intro_music");
// var exploreAudio = document.getElementById("start_explo");
var home_button = document.getElementById('homeButton');
var back_button = document.getElementById('backButton');

var homeContainer = document.getElementById('home-container');
var pingContainer = document.getElementById('ping-container');
var pongContainer = document.getElementById('pong-container');
var tempContainer = document.getElementById('temp_container');
var introAnimator = function()
{
	this.current_animation_frame = -1;
	this.animation_frames = [];
}


introAnimator.prototype.hide = function()
{
	$('#introVideo-contents').html('')
  $('#introVideo-controls').css('visibility', 'hidden')
	$('#introVideoOverlay').css('visibility', 'hidden')
}

introAnimator.prototype.set_animation_html = function()
{
	$('#introVideo-contents').html('<video id=introVideo autoplay loop width="100%" height="100%" controls><source src="content/' + this.animation_frames[this.current_animation_frame] + '" type="video/mp4" ></video>')

}

introAnimator.prototype.run = function(str)
{
    $(home_button).css('visibility', 'hidden')
    $(back_button).css('visibility', 'hidden')
    $('#home-container').css('visibility', 'hidden')

    $.idleTimer('pause');
		this.current_animation_frame = 0;
		this.animation_frames = str.split(':')
    $('#introVideo-controls').css('visibility', 'hidden')
    $('#introVideo-controls-reactivate').css('visibility', 'visible')
		$('#introVideoOverlay').css('visibility', 'visible')
		this.set_animation_html()
}

introAnimator.prototype.startExploration = function()
{
    $('#home-container').css('visibility','visible')

		$('#pong-container').css('visibility','hidden')
    $('#ping-container').css('visibility','hidden')
    $('#temp-container').css('visibility','hidden')


    $.idleTimer('reset');
    $('#introVideo-contents').html('')
    $('#introVideo-controls').css('visibility', 'hidden')
		$('#introVideoOverlay').css('visibility', 'hidden')
    $('#introVideo-controls-reactivate').css('visibility', 'hidden')
}

introAnimator.prototype.turnOFF = function()
{
    $('#introVideo-controls-reactivate').css('visibility', 'hidden')
}
