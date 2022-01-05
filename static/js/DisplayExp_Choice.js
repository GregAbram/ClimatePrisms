var DisplayExp_Choice = function()
{
    this.layout = "";  
}

DisplayExp_Choice.prototype.display = function(div_id)
{
    $.idleTimer('pause');

    $('#main_homePage').css('visibility', 'hidden')
    $('#choice_exploration').css('visibility', 'visible')

    $('#' + div_id).css('visibility', 'visible')

    this.layout = div_id;

}
