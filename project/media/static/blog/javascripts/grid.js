
function init_grid() {
	$(".grid .cell").click(function(){
		var id = $(this).attr("id").replace("cell_","");
		window.location = "#"+id;
		go_to_post(id);
	});             
	var anchor = $.url.attr("anchor");
	go_to_post(anchor);
	$(".grid").removeClass("hide");
}

function go_to_post(id) {
	var post = $("#"+id);
	if (post.size()) {
		$(".list .post").not(post).hide();
		post.show();
		$.scrollTo(post, {duration: 500});
	}
}