jQuery.fn.delay = function(time,func){
	this.each(function(){
		setTimeout(func,time);
	});
	
	return this;
};