var ThemeAnimator = function() {
    this.current_story = "";
    this.current_video = "";
}

ThemeAnimator.prototype.hide = function() {
    $('#themeVideo-contents').html('')
    $('#themeVideo-controls').css('visibility', 'hidden')
    $('#themeVideoOverlay').css('visibility', 'hidden')
    $(home_button).css('visibility', 'visible');
    $.idleTimer('reset');
}

ThemeAnimator.prototype.set_animation_html = function() {
    $('#themeVideo-contents').html('<video id="videoContainer" autoplay onended=state.themeAnimator.displayStories(); width="100%" height="100%" controls><source src="content/DATABASE/Video/' + this.current_video + '" type="video/mp4" ></video>')
}

ThemeAnimator.prototype.displayStories = function() {
    $('#themeVideo-contents').html('')
    $('#themeVideo-controls').css('visibility', 'hidden')
    $('#themeVideoOverlay').css('visibility', 'hidden')
    $(home_button).css('visibility', 'visible');
    $.idleTimer('reset');

}

ThemeAnimator.prototype.run = function(str, story_name) {
    $.idleTimer('pause');
    $('#themeVideoOverlay').css('visibility', 'visible')
    $('#themeVideo-controls').css('visibility', 'visible');
    $('#home-container').css('visibility', 'hidden')
    this.current_video = str;
    this.current_story = story_name;
    this.set_animation_html();

    findStory(this.current_story);
}
