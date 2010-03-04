
function go_to_post(id) {
	var post = $("#"+id);
	if (post.size()) {
		$(".list .post").not(post).hide();
		post.show();
		$.scrollTo($("#"+id), {duration: 500, offset: {top: -150}});
	}
}

function init_grid() {
	$.historyInit(go_to_post);
	$(".grid .cell").click(function(){
		var id = $(this).attr("id").replace("cell_","");
		window.location = "#"+id;
		$.historyLoad(id);
	});             
//	var anchor = $.url.attr("anchor");
//	go_to_post(anchor);
	$(".grid").removeClass("hide");
}

