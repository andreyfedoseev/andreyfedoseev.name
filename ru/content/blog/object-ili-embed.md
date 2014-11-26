Title: <object>, <embed> и валидный код
Date: 2010-03-05T02:00:00
Tags: веб-разработка
Slug: 25/object-ili-embed
Feed: false

<p>В детстве нас всех учили, что для встраивания флэша на страницу нужно пользоваться тегами <code>object</code> и <code>embed</code>. Объясняли это тем, что <code>object</code> используется Internet Explorer'ом на винде, а браузеры, основанные на Netscape понимают только <code>embed</code>.</p>
<p>Казалось бы, вставляй оба тега и будет счастье. Только вот счастья нет, потому что <code>embed</code> — это нестандартный тег, которого нет в спецификации HTML4.01 / XHTML1.0. (однако, он включён в черновик HTML5).</p>
<p>Но это ещё не вся <em>шокирующая правда</em>. Дело в том, что все более-менее современные браузеры поддерживают стандартный тег <code>object</code>.</p>
<!-- more -->
<p>В своём блоге я часто использую флэш, чтобы показывать видяшки и вставлять музыку. При этом я просто копирую под плеера с сайта и вставляю его в запись, либо использую <code>oembed</code> (о котором я скоро напишу заметку). В большинстве случаев этот кусок кода содержит оба тега, а иногда и вовсе только <code>embed</code>.</p>
<p>Все знают, что валидный HTML код — это <a href="http://andreyfedoseev.name/blog/post/12/pro-validnost-koda/">мой пунктик</a>. Поэтому я не стал терпеть этих невалидных корявок в своём собственном блоге и решил разобраться. Погуглив, я нашёл <a href="http://www.alistapart.com/articles/flashsatay/">рецепт</a> (написанный аж в 2002 году), описывающий, как вставлять объекты на страницу, используя при этом только валидный код. Вкратце суть его такова:</p>
<ol>
<li>Для тега <code>object</code> нужно указать атрибут <code>type</code>, например <code>type="application/x-shockwave-flash"</code>
<li>Также для <code>object</code> нужно указать атрибут <code>data</code>. В нём указывается URL  объекта, который вы хотите вставить</li>
<li>После этого нужно удалить тег <code>embed</code> нафиг</li>
</ol>
<p>Чтобы не заниматься такой чисткой вручную, я написал простенькую функцию, которая автоматически исправляет HTML код перед отображением на странице. Вот она:</p>

    #!python
    from BeautifulSoup import BeautifulSoup, Tag
    
    
    def fix_embeds(value):
        soup = BeautifulSoup(value)
    
        for object in soup.findAll("object"):
            movie = None
            for param in object.findAll("param"):
                if param["name"] == "movie":
                    movie = param["value"]
            embeds = object.findAll("embed")
            if embeds:
                embed = embeds[0]
            else:
                embed = None
            data = object.get("data")
            if not data:
                if movie:
                    object["data"] = movie
                elif embed and embed.get("src"):
                    object["data"] = embed["src"]
                else:
                    continue
            
            if not object.get("type") and embed.get("type"):
                object["type"] = embed["type"]
            del object["classid"]
            for embed in object.findAll("embed"):
                embed.extract()
        
        for embed in soup.findAll("embed"):
            src = embed.get("src")
            type = embed.get("type")
            if not src or not type:
                continue
            width = embed.get("width")
            height = embed.get("height")
            object = Tag(soup, "object")
            object["data"] = src
            object["type"] = type
            if width:
                object["width"] = width
            if height:
                object["height"] = height
            embed.replaceWith(object)
    
                    
        return unicode(soup)
        
<p>На её основе можно, например, сделать фильтр для шаблонов Django.</p>
<p>Обратите внимание, что я принудительно удаляю атрибут <code>classid</code> из тегов <code>object</code>. Его назначение остаётся для меня загадкой, однако если он присутствует, то не отображается музыкальный проигрыватель с Jamendo.</p>
<p>Пользуйтесь на здоровье. Если обнаружите какие-то косяки — пишите.</p>
<p><small>P.S. Теперь у меня полностью <a href="http://validator.w3.org/check?uri=http://andreyfedoseev.name/blog/">валидный бложек</a>.</small></p>
