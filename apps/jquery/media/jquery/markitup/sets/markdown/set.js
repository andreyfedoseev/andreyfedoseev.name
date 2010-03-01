// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// MarkDown tags example
// http://en.wikipedia.org/wiki/Markdown
// http://daringfireball.net/projects/markdown/
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------
markdownSettings = {
	previewParserPath:	'',
	onShiftEnter:		{keepDefault:false, openWith:'\n\n'},
	markupSet: [
		{name:'First Level Heading', key:'1', placeHolder:'Your title here...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '=') }, className: "h1Button"},
		{name:'Second Level Heading', key:'2', placeHolder:'Your title here...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '-') }, className: "h2Button"},
		{name:'Heading 3', key:'3', openWith:'### ', placeHolder:'Your title here...', className: "h3Button"},
		{name:'Heading 4', key:'4', openWith:'#### ', placeHolder:'Your title here...', className: "h4Button" },
		{name:'Heading 5', key:'5', openWith:'##### ', placeHolder:'Your title here...', className: "h5Button" },
		{name:'Heading 6', key:'6', openWith:'###### ', placeHolder:'Your title here...', className: "h6Button" },
		{separator:'---------------' },		
		{name:'Bold', key:'B', openWith:'**', closeWith:'**', className: "boldButton"},
		{name:'Italic', key:'I', openWith:'_', closeWith:'_', className: "italicButton"},
		{separator:'---------------' },
		{name:'Bulleted List', openWith:'- ', className: "ulButton"},
		{name:'Numeric List', openWith:function(markItUp) {
			return markItUp.line+'. ';
		}, className: "olButton"},
		{separator:'---------------' },
		{name:'Picture', key:'P', replaceWith:'![[![Alternative text]!]]([![Url:!:http://]!] "[![Title]!]")', className: "imageButton"},
		{name:'Link', key:'L', openWith:'[', closeWith:']([![Url:!:http://]!] "[![Title]!]")', placeHolder:'Your text to link here...', className: "linkButton"},
		{separator:'---------------'},	
		{name:'Quotes', openWith:'> ', className: "quoteButton"},
		{name:'Code Block / Code', openWith:'(!(\t|!|`)!)', closeWith:'(!(`)!)', className: "codeButton"},
		{separator:'---------------'},
		{name:'Preview', call:'preview', className:"preview"}
	]
};

// mIu nameSpace to avoid conflict.
miu = {
	markdownTitle: function(markItUp, char) {
		heading = '';
		n = $.trim(markItUp.selection||markItUp.placeHolder).length;
		for(i = 0; i < n; i++) {
			heading += char;
		}
		return '\n'+heading;
	}
};