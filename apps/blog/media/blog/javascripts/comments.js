(function() {
	
	function find_level($comment) {
		var level = $.grep($comment.attr('class').split(' '), function(el, idx) {
			if (el.indexOf('level') == 0) {
				return true;
			}
		});
		if (level.length > 0) {
			return parseInt(level[0].replace('level', ''));
		}
		return null;
	}
	
	window.CommentWidget = function(form_url, preview_url) {
		this.form_url = form_url;
		this.preview_url = preview_url;
		this.$form = null;
		this.working = false;
		var self = this;
		$("a#add-comment").click(function() {
			self.show_form();
			return false;
		});
		$(".comment a.reply").live('click', function() {
			var comment_id = $(this).parents(".comment").attr("id").replace("comment-", "");
			self.show_form(comment_id);
			return false;
		});
	};
	CommentWidget.prototype = {
		show_form: function(reply_to) {
			var $reply_to = null;
			if (reply_to != null) {
				$reply_to = $("#comment-" + reply_to)
			}
			if (this.$form != null) {
				this.$form.find("textarea[name='text']").val("");
				this.$form.find(".markItUpPreviewFrame").remove();
				this.$form.find(".error").remove();
				this.$form = this.$form.detach() 
				if ($reply_to != null) {
					$reply_to.after(this.$form);
					this.$form.find("input[name='reply_to']").val(reply_to);
				} else {
					$("#comments").append(this.$form);
					this.$form.find("input[name='reply_to']").val("");
				}
				this.$form.find(".indicator").hide();
				$.scrollTo(this.$form.find("a.anchor"), {duration: 500, offset: {top: -150}});
				this.$form.find(".comment-form").show('highlight', 1000);
			} else {
				if (this.working) {
					return;
				}
				this.working = true;
				var data = {}
				if (reply_to != null) {
					data.reply_to = reply_to;
				}
				var self = this;
				$.post(this.form_url, data, function(response, status, request) {
					self.$form = $(response);
					self.$form.find(".indicator").hide();
					self.init_comment_form();
					self.init_login_form();
					if ($reply_to != null) {
						$reply_to.after(self.$form);
					} else {
						$("#comments").append(self.$form);
					}
					$.scrollTo(self.$form.find("a.anchor"), {duration: 500, offset: {top: -150}});
					self.$form.find(".comment-form").show('highlight', 1000);
					self.working = false;
				});
			}
			
		},
		init_comment_form: function() {
			var self = this;
			this.$form.find("form.comment-form").submit(function() {
				self.submit_comment_form();
				return false;
			});
			var settings = $.extend(true, {}, markdownSettings);
			settings.markupSet = settings.markupSet.slice(7); 
			settings.previewParserPath = this.preview_url;
			this.$form.find("textarea[name='text']").markItUp(settings);
			this.$form.find("a.help").tooltip({
				showURL: false,
				top: 0,
				left: 20,
				extraClass: "rounded"
			});
			this.$form.find("a.help.noclick").click(function() {return false});
		},
		init_login_form: function() {
			return;
		},
		submit_comment_form: function() {
			if (this.working) {
				return false;
			}
			this.working = true;
			var $comment_form = this.$form.find("form.comment-form");
			var data = {};
			var reply_to = $comment_form.find("input[name='reply_to']").val();
			data.reply_to = reply_to;
			data.text = $comment_form.find("textarea[name='text']").val(); 
			data.author_name = $comment_form.find("input[name='author_name']").val(); 
			data.author_email = $comment_form.find("input[name='author_email']").val(); 
			data.author_url = $comment_form.find("input[name='author_url']").val();
//			data.notify = $comment_form.find("input[name='notify']").val();
			var self = this;
			self.$form.find(".indicator").show();
			$.post($comment_form.attr("action"), data, function(response, status, request) {
				var data = $.evalJSON(response);
				if (data.form) {
					$comment_form.replaceWith($(data.form));
					self.init_comment_form();
				} else if (data.comment) {
					var $comment = $(data.comment);
					var level = find_level($comment);
					if (level != null) {
						var $reply_to = $("#comment-"+reply_to);
						var inserted = false;
						var $followers = $reply_to.nextAll('.comment');
						for (var i = 0; i < $followers.length; i++) {
							var $follower = $($followers.get(i));
							var follower_level = find_level($follower);
							if (follower_level == null || follower_level < level) {
								$follower.before($comment);
								inserted = true;
								break;
							}
						}
						if (!inserted) {
							self.$form.after($comment);
						}
					} else {
						self.$form.after($comment);
					}
					self.$form.detach();
					self.$form.find(".indicator").hide();
					$.scrollTo($comment);
					$comment.show('highlight', 2000);
					$("#comments h4").show();
					self.working = false;
				}
			});
		}
	}
})();