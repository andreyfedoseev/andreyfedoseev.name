window.init_fancybox = ->
  $ ->
    $("figure a:has(img)").each((i, el)->
      $el = $(el)
      $el.fancybox(
        title: $el.find("img").attr("alt"),
        titleFormat: (title, currentArray, currentIndex, currentOpts)->
          title
      )
    )


window.init_blog_index = ->
  $ ->
    $links = $("nav.pages a");
    $next = $links.filter(".next")
    $prev = $links.filter(".prev")

    $(document).keypress((e)->
      if e.which == 63234 and e.ctrlKey and $prev.css("display") != "none"
        $prev.click()
      if e.which == 63235 and e.ctrlKey and $next.css("display") != "none"
        $next.click()
    )

    if not !!(window.history && history.pushState)
      return
    $entries_ct = $("#content div.entries")
    $title = $("title")
    base_window_title = $.trim($title.text().split("|").pop())

    pages = {}

    fetch_page = (url, callback=null, animated=true)->
      if url not of pages
        if animated
          $entries_ct.addClass("loading")

        suffix = "_=" + new Date().getTime();
        if url.indexOf("?") == -1
          _url = url + "?" + suffix
        else
          _url = url + "&" + suffix

        $.getJSON(_url, null, (data)->
          pages[url] = data
          if animated
            $entries_ct.removeClass("loading")
          if callback
            callback(data)
        )
      else
        if callback
          callback(pages[url])

    prefetch_pages = ->
      if $next.attr("href")
        fetch_page($next.attr("href"), null, false)
      if $prev.attr("href")
        fetch_page($prev.attr("href"), null, false)

    show_page = (url, next=false)->
      fetch_page(url, (data)->
        $entries_ct.hide()
        window.scrollTo(0, 0)
        $entries_ct.html(data.entries)
        $entries_ct.effect("drop", {mode: "show", direction: if next then "right" else "left"})
        if data.next_page
          $next.attr("href", data.next_page)
          $next.show()
        else
          $next.hide()
        if data.prev_page
          $prev.attr("href", data.prev_page)
          $prev.show()
        else
          $prev.hide()
        if data.page_title
          $title.text("#{data.page_title} | #{base_window_title}")
        else
          $title.text(base_window_title)
        prefetch_pages()
        window.init_fancybox())

    $links.click((e)=>
      e.preventDefault()
      $target = $(e.target)
      if $target.is("span")
        $target = $target.parent()
      next = $target.hasClass("next")
      url = $target.attr("href")
      $entries_ct.effect("drop", {direction: if next then "left" else "right"}, ->
        $entries_ct.show()
        $entries_ct.empty()
        url = $target.attr("href")
        history.pushState({next: next, url: url}, "", url)
        show_page(url, next)
        return
      )
    )

    $(window).bind("popstate", (e)->
      state = e.originalEvent.state
      if state
        next = state.next
        $entries_ct.effect("drop", {direction: if next then "left" else "right"}, ->
          $entries_ct.show()
          $entries_ct.empty()
          show_page(state.url, next)
        )
    )
    history.replaceState({next: false, url: window.location.href}, "", window.location.href)
    prefetch_pages()

    window.init_fancybox()


window.init_comment_form = ->

  $comments = $("#comments")
  $form = $("#comment-form")
  $text = $form.find("#id_text")
  $in_reply_to = $form.find("#id_parent")
  $buttons_ct = $form.find("div.buttons")
  $submit_btn = $buttons_ct.find("input[type='submit']")

  $footer_show_comment = $comments.find("footer a.show-comment-form")

  $("a.show-comment-form").click((e)->
    if $in_reply_to.val()
      $footer_show_comment.hide()
      $in_reply_to.val("")
      $form.hide().detach().insertAfter($comments.find("article.comment").last()).fadeIn()
  )

  $comments.delegate("a.reply", "click", (e)->
    $comment = $(this).closest("article.comment")
    id = $comment.data("id")
    if $in_reply_to.val() == ("" + id)
      return
    $in_reply_to.val(id)
    $form.hide().detach().insertAfter($comment).fadeIn()
    $footer_show_comment.show()
  )

  $comments.delegate("a.delete", "click", (e)->
    e.preventDefault()
    $target = $(this)
    $comment = $(this).closest("article.comment")
    level = $comment.data("lvl")
    thread = [$comment[0]]
    for c in $comment.nextAll("article.comment")
      l = $(c).data("lvl")
      if l > level
        thread.push(c)
      else
        break
    if thread.length == 1
      msg = gettext("Delete this comment?")
    else
      count = thread.length - 1
      msg = ngettext("Delete this comment and reply?",
                     "Delete this comment and %(count)s replies?",
                     count)
      msg = interpolate(msg, {count: count}, true)
    apprise(msg,
      verify: true,
      textYes: gettext("Yes"),
      textNo: gettext("No")
    (r)->
      if r
        $(thread).fadeOut()
        $.post($target.attr("href"), {}, (response)->
        )
    )
  )

  $form.find("a.markdown").qtip(
    content:
      text: ->
        $("#markdown-help").html()
    position:
      target: "event",
      my: "left top",
      at: "right center"
    style:
      classes: "markdown-help ui-tooltip-rounded ui-tooltip-plain"
      width: 400
  ).click((e)->
    e.preventDefault()
  )

  $preview_area = $form.find("#preview-area")

  markdown_converter = new Showdown.converter()

  $text.textareaPreview(
    container: $preview_area,
    enabled: false,
    preprocess: (text)->
      markdown_converter.makeHtml(text)
  )

  $preview_checkbox = $form.find("#id_preview")

  $preview_checkbox.change((e)->
    $this = $(this)
    if $this.attr("checked")
      $text.textareaPreview("enable")
    else
      $text.textareaPreview("disable")
  )

  $comments_header = $comments.find("header:first")

  $form.validate(
    rules:
      author_name:
        required: true,
        minlength: 4
      author_email: "email",
      author_url: "url",
      text:
        required: true,
        minlength: 4
    messages:
      author_name:
        required: gettext("This field is required.")
        minlength: gettext("Name is too short.")
      author_email:
        email: gettext("Enter a valid email address.")
      author_url:
        url: gettext("Enter a valid URL.")
      text:
        required: gettext("This field is required.")
        minlength: gettext("Text is too short.")
    submitHandler: (form)->
      $submit_btn.attr("disabled", "disabled")
      $buttons_ct.addClass("loading")
      $.post($form.attr("action"), $form.serialize(), (response)->
        if response.status == "success"
          $comment = $form.prev("article.comment")
          $text.val("")
          $in_reply_to.val("")
          $preview_area.html("").hide()
          if $comment.length
            $(response.comment).insertAfter($comment).fadeIn()
          else
            $(response.comment).insertAfter($comments_header).fadeIn()
          $form.detach().insertAfter($comments.find("article.comment").last())
        $buttons_ct.removeClass("loading")
        $submit_btn.removeAttr("disabled")
      )
    errorPlacement: (error, element)->
      error.appendTo(element.parents(".field").find(".errors"))
  )

