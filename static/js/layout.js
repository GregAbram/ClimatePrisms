var Layout = function()
{
	this.min_aspect							= 0.3;
	this.max_aspect							= 1.5;
	this.min_good   						= 0.6;
	this.max_good   						= 0.8;
	this.prop_subdivide					= 0.2;
	this.max_subdiv_level 			=3;
	this.min_stretch						= 0.1;

	this.max_images							= 5;

	this.min_width_proportion  	= 0.15;
	this.min_height_proportion  = 0.15;
	this.min_gap_proportion     = 0.02;

	// The following three are calculated for a given window size

	this.min_width 							= -1;
	this.min_height 						= -1;
	this.min_gap    						= -1;

}

Layout.prototype.random = function()
{
//	return 0.25;
	 return Math.random();
}

// Remove a specific member from an array

Layout.prototype.cull_array = function(a, i)
{
	if (i > a.length)
	{
		assert('cull array: removing ' + i + ' from array of length ' + a.length)
		return [];
	}

	var na = []
	for (var j = 0; j < a.length; j++)
		if (i != j) na.push(a[j]);

	return na;
}

// Find r, the scaling necessary to fit the image's far corner to the
// rect's boundary (that is, fitting it into the rect as best as possible
// without stretching).  This will result in gaps either at the bottom or
// right, depending on the difference between the aspect ratios.

Layout.prototype.scale = function(image, rect)
{
	var iw = image.width;
	var ij = image.height;

	var r = rect.rw/image.width;
	var h = image.height * r;

	if (h > rect.rh)
		return rect.rh/image.height;
	else
		return r;
}

// Given that r, subdiv moves the corner randomly into the 'golden' region.

Layout.prototype.subdiv = function(r)
{
	return r * (this.min_good + this.random()*(this.max_good - this.min_good));
}

// Can the given image be stretched into the given rect based on the
// min_stretch interval around 1.0?

Layout.prototype.can_stretch = function(ix, iy, rx, ry)
{
	var r = (ix/iy) / (rx/ry);
	var s = (r < (1.0 + this.min_stretch)) && (r > (1.0 - this.min_stretch))
	return s;
}

// Given that original, un-subdivved r and the current tiling level,
// decide whether to subdiv.

Layout.prototype.subdiv_test = function(i, r, image, rect)
{
	return i == 0;
/*
	// Don't, if we have passed some level limit

	if (i >= this.max_subdiv_level)
	{
		return false;
	}

	// Don't, if the current r results in the expected value
	// of the result would  fall below some minimal size.

	var iw = ((this.min_good + this.max_good) / 2.0) * r * image.width;
	var ih = ((this.min_good + this.max_good) / 2.0) * r * image.height;

	if (iw < this.min_width || ih < this.min_height)
		return false;

	// Is stretching this image to fit the rect exactly tolerable?

	var stretchable = this.can_stretch(iw, ih, rect.x, rect.y)

	// Do, if its not stretchable, and the result would leave
	// sliver gaps

	if (!stretchable && (((rect.w - iw) < this.min_gap) || ((rect.h - ih) < this.min_gap)))
		return true;

	// If conditions have not already dictated a case, then
	// we subdiv based on the prop_subdivide value;

	var p = this.random() < this.prop_subdivide;
	return p;
*/
}

Layout.prototype.createTiles = function(content)
{
	var rects = [];
	rects.push({x: 0, y: 0, rw: $(window).width(), rh: $(window).height(), empty: true});

	this.min_width 				= this.min_width_proportion * $(window).width();
	this.min_height 			= this.min_height_proportion * $(window).height();
	this.min_gap    			= this.min_gap_proportion * $(window).width();

	var tiling = [];
	for (var tnum = 0; tnum < content.length && tiling.length < this.max_images; tnum++)
	{
		var image = content[tnum];

		if (rects.length == 0)
			break;

		// For each available rect, find the one that best suits this image.
		// It'll be the one that the current image is largest when scaled into
		// the rect.

		var best_s = -1;
		var best_r = -1;
		for (var r = 0; r < rects.length; r++)
		{
			var rect = rects[r];

			// Whats the scaling factor necessary to fit this image into this
			// tile?

			s = this.scale(image, rect);

			if (s*image.width < this.min_width || s*image.height < this.min_height)
				continue;

			// Look for the largest.

			if (best_r == -1 || best_s < s)
			{
				best_r = r;
				best_s = s;
			}
		}

		if (best_r == -1)
			continue;

		var rect = rects[best_r];

		var rx = rect.x;	// Rectangle sizes.  These are fixed.
		var ry = rect.y;
		var rw = rect.rw;
		var rh = rect.rh;

		// Should we subdivide the scaling to move the image corner into the
		// 'golden zone'?  No, if there is no content left to fit. Otherwise,
		// apply the rules above.

		var iw, ih;

		if (tiling.length < (content.length-1) && this.subdiv_test(tiling.length, best_s, image, rect))
		{
			var s = this.subdiv(best_s);
			iw = s * image.width;
			ih = s * image.height;
		}
		else if (this.can_stretch(image.width, image.height, rw, rh))
		{
			iw = rw;
			ih = rh;
		}
		else
		{
			iw = best_s * image.width;
			ih = best_s * image.height;
		}

		var gw = rw - iw;
		var gh = rh - ih;

		// justification (won't do anything if the gap size is 0

		var il, ib;

		if (this.random() > 0.5) il = 0;
		else il = gw;

		if (this.random() > 0.5) ib = 0;
		else ib = gh;

		var new_tile;
		var new_rects;

		if (gw > 0 && gh > 0)
		{
			// then we need to add 2 rects - which?  r = 0 favors X
			var r = (this.random() > 0.5);

			var blank0, blank1;

			if (il == 0)
			{
				if (ib == 0)
				{
					if (r)
					{
						blank0 = {x: rx + iw, y: ry,          rw: gw,    rh: rh, 	empty: true};
						blank1 = {x: rx,      y: ry + ih,     rw: iw,    rh: gh, 	empty: true};
					}
					else
					{
						blank0 = {x: rx + iw, y: ry,          rw: gw,    rh: ih,	empty: true};
						blank1 = {x: rx,      y: ry + ih,     rw: rw,    rh: gh, 	empty: true};
					}
				}
				else
				{
					if (r)
					{
						blank0 = {x: rx + iw, y: ry,           rw: gw,   rh: rh, 	empty: true};
						blank1 = {x: rx,      y: ry,           rw: iw,   rh: gh, 	empty: true};
					}
					else
					{
						blank0 = {x: rx + iw, y: ry,           rw: gw,   rh: rh, 	empty: true};
						blank1 = {x: rx,      y: ry,           rw: iw,   rh: gh, 	empty: true};
					}
				}
			}
			else
			{
				if (ib == 0)
				{
					if (r)
					{
						blank0 = {x: rx,        y: ry,         rw: gw,   rh: rh, 	empty: true};
						blank1 = {x: rx + gw,   y: ry + ih,    rw: iw,   rh: gh, 	empty: true};
					}
					else
					{
						blank0 = {x: rx,        y: ry,         rw: gw,   rh: ih,	empty: true};
						blank1 = {x: rx,        y: ry + ih,    rw: rw,   rh: gh, 	empty: true};
					}
				}
				else
				{
					if (r)
					{
						blank0 = {x: rx,        y: ry,         rw: gw,   rh: rh, 	empty: true};
						blank1 = {x: rx + gw,   y: ry,         rw: iw,   rh: gh, 	empty: true};
					}
					else
					{
						blank0 = {x: rx,        y: ry,         rw: rw,   rh: gh, 	empty: true};
						blank1 = {x: rx,        y: ry + gh,    rw: gw,   rh: ih,	empty: true};
					}
				}
			}

			new_rects = [blank0, blank1];

			image.x   = rx + il;
			image.y   = ry + ib;
			image.rw  = iw;
			image.rh  = ih;
		}
		else
		{
			// Divide either horizontally or vertically, stretching in the other direction.
			// Crate blank.  Choose to offset either image or blank randomly

			image.x = rx;
			image.y = ry;
			image.rw = iw;
			image.rh = ih;

			if (gw > 0)
			{
				image.rh = rh;   // Stretch in Y
				var blank = {x: rx, y: ry, rw: gw, rh: ih+gh, empty: true};

				if (r > 0.5)
					blank.x = blank.x + iw;
				else
					image.x = image.x + gw;

				new_rects = [blank];
			}
			else
			{
				image.rw = rw; // Strectch in X
				var blank = {x: rx, y: ry, rw: iw+gw, rh: gh, empty: true};

				if (r > 0.5)
					blank.y = blank.y + ih;
				else
					image.y = image.y + gh;

				new_rects = [blank];
			}
		}

		tiling.push(image);

		rects = new_rects.concat(this.cull_array(rects, best_r));
	}

	return tiling.concat(rects);
}
