(function() {
	function beforeUpload(file, extension) {
		if (!(extension && /^(jpg|png|jpeg|gif)$/i.test(extension))) {
			// extension is not allowed
			alert('Error: invalid file extension');
			// 	cancel upload
		return false;
		}
		this.widget.button.addClass("loading");
	}
	
	function afterUpload(file, response) {
		var response = $.evalJSON(response);
		if (response.status == 'failure') {
			var div = $('<div class="notification error">'+response.message+'</div>');
			div = $("#notifications").append(div);
			div.delay(5000, function() {this.fadeout();})
		} else {
			this.widget.updateImages(response);
			var div = $('<div class="notification success">'+response.message+'</div>');
			$("#notifications").append(div).delay(5000, function() {div.fadeOut();});
		}
//		this.widget.button.removeClass("loading");
	}
	
	IMAGE_ID_PREFIX = "images-widget-image-";
	TEMPLATE = $.template('<div class="image-container" id="${id}">' +
	  '<div class="wrapper"><img src="${src}" /></div>'+
	  '<a class="insert-image-button original" href="javascript:void(0);"></a>'+
	  '<a class="insert-image-button scaled" href="javascript:void(0);"></a>'+
	  '<a class="insert-image-button thumb" href="javascript:void(0);"></a>'+
	  '<a class="delete" href="javascript:void(0);"></a></div>').compile();
	TEMPLATE_ORIGINAL = $.template('{% image ${id} original "[![Alt:!:${filename}]!]" %}').compile();
	TEMPLATE_THUMB = $.template('{% image ${id} thumb "[![Alt:!:${filename}]!]" %}').compile();
	TEMPLATE_SCALED = $.template('{% image ${id} scaled "[![Alt:!:${filename}]!]" %}').compile();
	
	window.ImagesWidget = function(button, upload_url, get_images_url, delete_image_url, field) {
		this.button = $(button);
		this.data = {};
		this.get_images_url = get_images_url;
		this.delete_image_url = delete_image_url;
		this.field = $("input[name='"+field+"']");
		this.uploader = new AjaxUpload(this.button, {
			action : upload_url,
//			responseType : "json",
			onSubmit : beforeUpload,
			onComplete: afterUpload
		});
		this.uploader.widget = this;
		this.loadImages();
	};
	ImagesWidget.prototype = {
		loadImages: function(id) {
			if (id) {
				var ids = [id];
			} else {
				var ids = this.field.attr("value").split(",");
			}
			if (ids.length == 0) {
				$("#images-widget .images-container").hide();
				return;
			}
			var self = this;
			$.getJSON(this.get_images_url, {ids: ids}, function(data) {
				for (var i = 0; i < data.length; i++) {
					var image = data[i];
					self.data[image.id] = image;
					var id = IMAGE_ID_PREFIX + image.id;
					var src = image.thumb_url;
					$("#images-widget .images-container").append(TEMPLATE, {id: id, image_id: image.id, src: src});
					$("#"+id+" img").click(function() {
						var data = self.data[$(this).parents(".image-container").attr("id").slice(IMAGE_ID_PREFIX.length)];
						var $modal = $('img[src$="'+data.scaled+'"]');
						if ($modal.length) {
							$modal.dialog('open');
						} else {
							var img = $('<img style="display:none;padding: 8px;" />').attr('src',data.scaled_url).appendTo('body');
							setTimeout(function() {
								img.dialog({
										width: 515,
										modal: true
									});
							}, 1);
						}				
					});
					$("#"+id+" a.insert-image-button.thumb").click(function() {
						var data = self.data[$(this).parent(".image-container").attr("id").slice(IMAGE_ID_PREFIX.length)];
						$.markItUp({target: '.markitup',
							replaceWith: TEMPLATE_THUMB.apply({
								id: data.id,
								filename: data.filename
							})
						});
					});
					$("#"+id+" a.insert-image-button.scaled").click(function() {
						var data = self.data[$(this).parent(".image-container").attr("id").slice(IMAGE_ID_PREFIX.length)];
						$.markItUp({target: '.markitup',
							replaceWith: TEMPLATE_SCALED.apply({
								id: data.id,
								filename: data.filename
							})
						});
					});
					$("#"+id+" a.insert-image-button.original").click(function() {
						var data = self.data[$(this).parent(".image-container").attr("id").slice(IMAGE_ID_PREFIX.length)];
						$.markItUp({target: '.markitup',
							replaceWith: TEMPLATE_ORIGINAL.apply({
								id: data.id,
								filename: data.filename
							})
						});
					});
					$("#"+id+" > a.delete").click(function() {
						var id = $(this).parent(".image-container").attr("id").slice(IMAGE_ID_PREFIX.length);
						var delete_image_url = self.delete_image_url;
						var dialog = $("#delete-image-dialog");
						if (!dialog.length) {
							dialog = $('<div id="delete-image-dialog"></div>').appendTo('body'); 
							dialog.dialog({
								title: gettext("Delete this image?"),
								bgiframe: true,
								resizable: false,
								modal: true,
								height: 1,
								minHeight: 1,
								overlay: {
									backgroundColor: '#000',
									opacity: 0.5
								},
							});
						}
						var buttons = {};
						buttons[gettext("Delete")] = function() {
							$.getJSON(delete_image_url, {id: id}, function(data) {
								$("#"+IMAGE_ID_PREFIX+id).remove();
								var ids = self.field.attr("value").split(",");
								var new_ids = [];
								for (var i = 0; i < ids.length; i++) {
									if (ids[i] != id) {
										new_ids.push(ids[i]);
									}
								}
								self.field.attr("value", new_ids.join(","));
							});
							$(this).dialog('close');
						};
						buttons[gettext("Cancel")] = function() {
							$(this).dialog('close');
						}; 
						dialog.dialog("option", "buttons", buttons);
						dialog.dialog("open");
					});
				}
				if (data.length > 0) {
					$("#images-widget .images-container").show();
				}
				self.uploader.widget.button.removeClass("loading");
			});
		},
		updateImages: function(data) {
			ids = this.field.attr("value").split(",");
			ids.push(data.id);
			this.field.attr("value", ids.join(","));
			this.loadImages(data.id);
		},
	}
})();