/**
 * Inline label v1.1.1
 * Tested with jQuery 1.3.x and 1.4.x.
 * Released under CC-BY-SA http://creativecommons.org/licenses/by-sa/2.5/se/
 * 
 * Usage: 	$('#id').inline_label();
 * 			$('#id').inline_label({text: "yada yada"}); // use text instead of label text
 * 			$('#id').inline_label({use_title: true}); // use the title instead of label text
 * 			$('#id').inline_label({css_class: "my_inline_label"}); // which class to add
 * 			$('#id').inline_label({hide_label: false}); // whether to hide the label or not
 * 
 * When using the text option, hide_label makes no difference.
 * 
 */
(function($) {
	$.fn.inline_label = function(options) {
		// default settings
		var config = {
			text: false,
			use_title: false,
			css_class: "inline_label",
			hide_label: true
		};
		if (options) $.extend(config, options);
		
		this.each(function() {
			var t = $(this);
			var text;
			if (config.text) {
				// if a text is defined, use that
				text = config.text;
			} else if (config.use_title) {
				text = t.attr('title');
			} else {
				// otherwise use the labels text
				if (!t.attr('id')) {
					throw "No id attribute found!";
				}
				var label = $('label[for='+t.attr('id')+']');
				// sanity checks
				if (label.length == 0) {
					throw "No label for "+t.attr('id')+"!";
				}
				if (label.length > 1) {
					throw "Too many labels for "+t.attr('id')+"!";
				}
				
				text = label.text();
				if (config.hide_label) {
					label.hide();
				}
			}
			
			// set up the focus hook
			t.focus(function() {
				var t = $(this);
				if (t.val() == text) {
					t.val('');
					if (config.css_class) {
						t.removeClass(config.css_class);
					}
				}
			});
			
			// set up the blur hook
			t.blur(function() {
				var t = $(this);
				if (t.val() == '') {
					t.val(text);
					if (config.css_class) {
						t.addClass(config.css_class);
					}
				}
			});
			// bugfix from sendai, focus before bluring
			t.trigger('focus');
			t.trigger('blur');
		});
		
		return this;
	};
})(jQuery);