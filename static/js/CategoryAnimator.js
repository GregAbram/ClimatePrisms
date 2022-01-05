var CategoryAnimator = function()
{
    this.current_story = "";
    this.current_video = "";
}

CategoryAnimator.prototype.hide = function()
{
	$('#categoryVideo-contents').html('')
  $('#categoryVideo-controls').css('visibility', 'hidden')
	$('#categoryVideoOverlay').css('visibility', 'hidden')
  $(home_button).css('visibility', 'visible');
  $.idleTimer('reset');
}

CategoryAnimator.prototype.set_animation_html = function()
{
	$('#categoryVideo-contents').html('<video id="videoContainer" autoplay onended=state.categoryAnimator.displayStories(); width="100%" height="100%" controls><source src="content/DATABASE/Video/' + this.current_video + '" type="video/mp4" ></video>')
}

CategoryAnimator.prototype.displayStories = function()
{
  $('#categoryVideoOverlay').css('visibility', 'hidden');
  $('#categoryVideo-controls').css('visibility', 'hidden')
  $('#categoryVideo-contents').html('')
  $(home_button).css('visibility', 'visible');
  $.idleTimer('reset');
}

CategoryAnimator.prototype.run = function(str, story_name)
{
    $.idleTimer('pause');
	  $('#categoryVideoOverlay').css('visibility', 'visible')
    $('#categoryVideo-controls').css('visibility', 'visible')
    $('#home-container').css('visibility', 'hidden')
    this.current_video = str;
    this.current_story = story_name;
    this.set_animation_html();
    findTag(this.current_story);
}
