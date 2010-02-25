var n_speed = 200     
var is_index = false
var a_images = [] 
var n_current_image = 0 
var view
var previous_page = "no"
var next_page = "no"   
var is_loading_next = false    
var current_page = 0 
//
function init(){
	$(".post_thumb").click(function(){
		var id = $(this).attr("id").replace("thumb_","")
		window.location = "#"+id
	})             
	//
	$("#search_field").keydown(function(e){
		if(e_.which == 13){
			$("#search_field").submit()
		}
	})
	$("#loading").fadeTo(n_speed, 0)
	if($.cookie("view") == null){
		view = default_format
		$.cookie("view", view)
	}else{
		view = $.cookie("view") 
		default_format = view
	}  
	if(is_index){
		if(view == "grid"){
			$(".grid").removeClass("hide")
			$("#view_options").html("<li><a href=\"#list\" id=\"show_list_link\" class=\"rounded\">Display as list.</a></li>")	
			$("#show_list_link").click(show_list)        
			getVideoThumbs();    
		}else{        
			$("#entry").addClass("hide")   
			$(".line").addClass("hide") 
			$(".list").removeClass("hide")             
			$("#view_options").html("<li><a href=\"#grid\" class=\"rounded\" id=\"show_grid_link\">Display as grid.</a></li>")
			$("#show_grid_link").click(show_grid)
			$(window).scroll(check_for_more);
		}
	 	SWFAddress.addEventListener(SWFAddressEvent.CHANGE, history);
	}else{
		format_notes();
		$("#dsq-options").remove()
		$(".dsq-by").remove()           
	}    
}
//
function history(hash){
	var id = SWFAddress.getValue()+""     
	if(id == "/"){
		//
	}else if(id == "about"){
		if(view == "list"){
			show_grid()
		}else{
			$(".line").removeClass("hide")  
			$("#entry").removeClass("hide")
			$("#entry").html(""+$("#about").html())   
		}
	}else if(id == "following"){
		if(view == "list"){
			show_grid()
		}else{
			$(".line").removeClass("hide")  
			$("#entry").removeClass("hide")
			$("#entry").html(""+$("#following").html())   
		}
	}else if(id == "search"){
		if(view == "list"){
			show_grid()
		}else{
			$(".line").removeClass("hide")  
			$("#entry").removeClass("hide")
			$("#entry").html(""+$("#search").html())   
		}
	}else{
		goto_post(id)		
	}      
}
//
function goto_post(id){
	if(view == "list"){
		show_grid()
	}
	$("#thumb_"+id+" .loading").fadeTo(0, 0)
	$("#thumb_"+id+" .loading").removeClass("hide")
	$("#thumb_"+id+" .loading").fadeTo(n_speed, 1)
	//$("#entry").fadeTo(n_speed, .1)
	$("html body").animate({
		scrollTop:0
	}, n_speed)
	var src = "/post/"+id+"/"
	if($("#entry").hasClass("hide")){
		$("#entry").removeClass("hide")
	}
	if($(".line").hasClass("hide")){
		$(".line").removeClass("hide")			
	}	                       
	$("#entry").html($("#"+id).html())     
	$("#entry").fadeTo(0, 0)
	if($("#entry").hasClass("hide")){
		$("#entry").removeClass("hide")
	}
	$("#entry").fadeTo(200, 1)
	$(".post_thumb").each(function(){
		if($(this).attr("id") == "thumb_"+id){
			if(!$(this).hasClass("selected")){
				$(this).addClass("selected")
			}
		}else{
			if($(this).hasClass("selected")){
				$(this).removeClass("selected")
			}
		}
	})   
	return false
}
//
function show_list(){    
	$.cookie("view", null);
	$.cookie("view", "list")      
	SWFAddress.setValue("")
	setTimeout("window.location.reload()", 10);
	return false
}   
//
function show_grid(){
	$.cookie("view", null);
	$.cookie("view", "grid")
	setTimeout("window.location.reload()", 10);
	return false
}
//            
function getVideoThumbs(){
	$(".list .video").each(function(){    
		var swf = "" 
		var id = $(this).parent().parent().attr("id")
		$(this).children("object").children("param").each(function(){
			if($(this).attr("name") == "movie"){
				swf = $(this).attr("value")
			}
		})                                
		if(swf.indexOf("youtube.com") >= 0){        
			// get youtube thumb
			swf = swf.replace("http://www.youtube.com")
			swf = swf.replace("http://youtube.com")
			var youtube_id = swf.substring(swf.indexOf("/v/")+3, swf.indexOf("&"))
			var thumb_url = "http://i.ytimg.com/vi/"+youtube_id+"/0.jpg"
			$("#thumb_"+id+" .video").prepend("<div class=\"bg rounded\" style=\"background-image:url('"+thumb_url+"');\"></div>")
		}else if(swf.indexOf("vimeo.com") >= 0){
			// get vimeo json, then thumb (SO ANNOYING!)
			swf = swf.replace("http://vimeo.com/moogaloop.swf?")
			swf = swf.replace("http://www.vimeo.com/moogaloop.swf?")      
			var vimeo_id = swf.substring(swf.indexOf("clip_id=")+8, swf.indexOf("&"));
			$.getJSON("http://vimeo.com/api/clip/"+vimeo_id+".json?callback=?", function(d){
				var thumb_url = d[0].thumbnail_large
				$("#thumb_"+id+" .video").prepend("<div class=\"bg rounded\" style=\"background-image:url('"+thumb_url+"');\"></div>")
			})
		}
	})
}      
//
function check_for_more(){
	if(view == "list"){ 
		var yPos = window.pageYOffset;
		var h = $(document).height()
		var wH = $(window).height()
		//$("#debug").text(yPos+" / "+h)
		if((yPos/(h-wH)) >= .8 && !is_loading_next && next_page != "no"){
			//alert("we're trying to load the next shit.")
			is_loading_next = true   
			$("html body").append("<div id=\"temp\" class=\"hide\"></div>")
			$(".list").append("<div id=\"next_"+current_page+"\"><div class=\"post_preloader\">loading next page...</div></div>") 
			$("#temp").load(next_page, {}, function(d){
				$(".post_preloader").remove()
				var content = $(d).children("#main_column .list").html()  
				$("#next_"+current_page).html(content)
				var n_p = $(d).children("#info .next_page").text()
				if(n_p != ""){
					next_page = n_p;
				}else{
					next_page = "no"
				} 
				setTimeout(can_check_for_more_now, 2000)
			})
		}
	}
}
//
function can_check_for_more_now(){     
	$(".post_preloader").remove()
	current_page++	
	is_loading_next = false    
}
//     
function format_notes(){
	$(".avatar").each(function(){
		$(this).parent().remove()
	})
}
//
function add_credit(){
	$("html body").append("<div id=\"credit\"><a href=\"http://cargotheme.tumblr.com\">Cargo Theme</a> by <a href=\"http://jarredbishop.tumblr.com\">Jarred Bishop</a>. Inspired by <a href=\"http://cargocollective.com\">Cargo</a></div>")
}
$(document).ready(init)  
$(document).load(loaded)