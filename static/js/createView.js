// CreateView.js August 10

var current_story_count = 0;

function random() {
    return Math.random();
    // return 0.25;
}

function createView(state, contents) {

    closeAllOverlays(); // close all captions and image enlargement to create view

    state.properties = getProperties(contents); //fill the properties data structure

    state.candidate_images = [];
    for (var i = 0; i < state.properties.length && i < 6; i++) {
        var prop = state.properties[i];
        state.candidate_images.push(prop);
    }

    var image_list = [];
    for (var i in state.candidate_images)
        image_list.push({
            name: "content/" + state.candidate_images[i].folder + "/" + state.candidate_images[i].image,
            index: i
        });

    ImageLoader.init(image_list, imagesLoaded, state)  // load images with attributes from imageloaer
    ImageLoader.start($('#temp'))
}

function imagesLoaded(ids, data) {

    var original_candidate_images = state.candidate_images;

    state.candidate_images = []
    for (var i in ids) {
        var c = original_candidate_images[ids[i].index];
        c.width = ids[i].width;
        c.height = ids[i].height;
        state.candidate_images.push(c);
    }

    state.tiled_images = state.layout.createTiles(state.candidate_images);
    var html = createHTML(state);
    post_layout(html);
}

function getProperties(nodes) {
    properties = new Array();

    for (var i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        var p = {
            level: n.level,
            tags: n.tagmain + ',' + n.tagmain2 + ',' + n.subcategory,
            color: n.color,
            meta: n.provenance,
            image: n.filename,
            context: n.context,
            enlarge_image: n.enlarge_image,
            rollover_image: n.rollover,
            content: n.content,
            area: n.area,
            folder: n.folder,
            crop: n.crop,
            texture: n.texture,
            name: n.caption,
            width: n.width,
            height: n.height,
            story: n.story,
            content_type: n.content_type,
            keyword: n.keyword,
            json: JSON.stringify(n)
        };

        // Eliminate duplicates

        for (var j = 0; j < properties.length; j++)
            if (p.image == properties[j].image)
                break;

        if (j == properties.length)
            properties.push(p);
    }

    return properties;
}

function getKeywordProperties() {
    keywordProperties = new Array();

    for (var i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        var p = {
            image: n.filename,
            keyword: n.keyword
        };

        // Eliminate duplicates

        for (var j = 0; j < properties.length; j++)
            if (p.image == properties[j].image)
                break;

        if (j == properties.length)
            properties.push(p);
    }

    return properties;
}

function createTiles(candidate_images) {
    var croppable_images = new Array();
    var texture_images = new Array();
    var content_images = new Array();

    for (var i in candidate_images) {
        image = candidate_images[i];
        if (image.texture == 'Y')
            if (image.crop == 'Y')
                croppable_images.push(image);
            else
                texture_images.push(image);
        else
            content_images.push(image);
    }

    var candidate_images = content_images.concat(texture_images).concat(croppable_images);

    // candidate_images = [candidate_images[0]];

    var tiled_images = createLayout(candidate_images);

    return tiled_images;
}

function closeAllOverlays() {
    $('#container').find(".info_popup").css("visibility", "hidden");
    $('#container').find(".image_popup").css("visibility", "hidden");
}

function popup_info(e, i) {

    //hide all other captions or enlarged image
    closeAllOverlays();

    //show pop info
    e.parent().find("#" + i).css('visibility', 'visible');
}

function popdown_info(e, i) {
    e.parent().parent().css('visibility', 'hidden');
}

function popup_image(a, e) {
    //hide all other captions or enlarged image
    closeAllOverlays();

    //show enlarfed image
    a.parent().find("#" + e).css('visibility', 'visible');
}

function popout_image(a, e) {
    $('#' + e).css('visibility', 'hidden');
}


//LAYOUT CREATION BY PASSING HTML to Post_layout
function createHTML(state) {
    var images = state.tiled_images;
    // Colors for "images" without content - e.g. empty rects
    var colors = ['darkgrey'];
    current_story_count = current_story_count + 1;
    html = '';

    var img_id = 0;
    for (var i in images) {
        var image = images[i];

        var divid = '"div_' + img_id + '"';
        var capid = '"cap_' + img_id + '"';
        var imgid = '"img_' + img_id + '"';
        var infid = '"inf_' + img_id + '"';

        var x = image.x;
        var y = image.y;
        var rw = image.rw;
        var rh = image.rh
        var iw = image.rw;
        var ih = image.rh;

        if (image.empty) {

            var b = state.fillers[Math.floor(random() * 0.99 * state.fillers.length)];

            var w = rw / b.width;
            var h = rh / b.height;

            var s;
            if (w > h) s = w;
            else s = h;

            var iw = s * b.width;
            var ih = s * b.height;

            html += '<div id=' + divid + ' style="overflow:hidden;position:absolute;left:' + x + 'px;top:' + y + 'px;width:' + rw + 'px;height:' + rh + 'px; background-color:black">';
            html += '  <img style="width:' + iw + 'px;height:' + ih + 'px;" src="' + b.fname + '" class=shadowOver "/>';
            html += '</div>';

        }
        else
        {
            var info = image.name;
            var textOnImage = image.enlarge_image == 1;


            var div = '<div id=' + divid + ' style="background-color:black;position:absolute;left:' + x + 'px;top:' + y + 'px;width:' + rw + 'px;height:' + rh + 'px)">';
            var img = '<img id=' + imgid + ' style="width:' + rw + 'px;height:' + rh + 'px" onmouseout=this.style.opacity=1; onmouseover=this.style.opacity=0.95; src="content/' + image.folder + "/" + image.image + '", onclick=\'loadSelectedContent(event, ' + image.json + ');\' />';

            html = html + div + img;

            if (info != "") {
                info;
                html += '<div id=' + infid + ' class=info_popup style="font-family:Sans-serif,Arial,Sans;font-size:32px;visibility:hidden;top:0px;left:0px;width:100%;height:100%">';
                html += '<div style="position:absolute;margin:10px;bottom:0px;right:20px;left:40px;padding-left:10px;background-color:#A19E6C;opacity:0.9;z-index:1010;padding:10px;">';
                html += '<p style="color:white">' + info + '</p>';
                html += '<div id=close style="visibility:inherit;position:absolute;margin:10px;bottom:0px;right:40px;width:100%;height:100%"background-color:#F5EED7;opacity:0.1;z-index:1002;padding:14px;" onmouseout=' + "'popdown_info($(this), " + infid + ")'" + '>';
                html += '</div>';
                html += '</div>';
                html += '</div>';
                html += '<img style="position:absolute;left:' + (rw - 85) + 'px;top:' + (rh - 85) + 'px;width:80px;height:80px;" onmouseover=' + "'popup_info($(this), " + infid + ")'" + ' src="icons/icon.png"/>';
            }

            // for enlarging images beyond its div container. Images have been assign a 1 or 0 with text that need to be enlarged for reading purposes.
            if (textOnImage != 0) {
                html += '<div id=' + capid + ' class=image_popup style="visibility:hidden;top:0px;left:0px;width:100%;height:100%;margin:auto;">';
                html += '<div id="enlarged" style="text-align:center;z-index:1000;position:relative;" onclick=' + "'popout_image($(this), " + capid + ");'>";
                html += '<img id="enlarged_image" style="position: fixed;top: 0;bottom: 0;left: 0;right: 0;max-width: 100%;max-height: 100%;margin: auto;overflow: auto;" onclick=' + "'popout_image($(this), " + capid + ");'" + 'src="content/' + image.folder + "/" + image.image + '">';
                html += '<img id="close_Enlarge" style="width:80px;height:70px;top:40px;position:fixed;right:35px;" src="icons/exitTwo.png"  onclick=' + "'popout_image($(this), " + capid + ");'>";
                html += '</div>'; //close imageEnlarge
                html += '<div id="background_Enlarge" style="position:fixed;top:0px;left:0px;width:100%;height:100%;background-color:black;opacity:0.8;z-index:1">';
                html += '</div>';
                html += '</div>';
                html += '<img style="position:absolute;right:' + (rw - 80) + 'px;top:' + (rh - 80) + 'px;width:70px;height:70px" onclick=' + "'popup_image($(this)," + capid + ");'" + 'src="icons/enlarge.png"/>';
            }

            html += '</div>';
            html += '</div>';
        }

        img_id++;
    }

    return html;
}
