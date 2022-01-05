function __imageLoader()
{
	this.init = function(images, after, data) 
	{
		this.elapsed 		= 0;
		this.count			= images.length;
		this.indices		= [];
		this.after			= after;
		this.data				= data;

		this.html = '';
		for (var i in images)
			this.html += '<img onload="ImageLoader.item_loaded(this)" onerror="ImageLoader.item_error(this)" id="id_' + i + '" src="' + images[i].name + '">';
	}

	this.start = function(div)
	{
		div.html(this.html);
	};

	this.item_loaded = function(me) 
	{
		this.count = this.count - 1;
		img = $(me);
		this.indices.push({index: img.attr('id').split('_')[1], width: img.width(), height: img.height()});
		if (this.count == 0)
			this.after(this.indices, this.data);
	};

	this.item_error = function(me) 
	{
//        alert("item_error error");
		this.count = this.count - 1;
		if (this.count == 0)
			this.after(this.indices, this.data);
	};
};

ImageLoader = new __imageLoader();
