
window.init_highlight = ->
  $ ->
    $("pre code").each((i, el)->
      hljs.highlightBlock(el, '    ')
    )

window.init_blog_index = ->
  $ ->
    if not History.enabled
      return
    $links = $("nav.pages a");
    $next = $links.filter(".next")
    $prev = $links.filter(".prev")
    $entries_ct = $("#content div.entries")
    $title = $("title")
    base_window_title = $.trim($title.text().split("|").pop())

    pages = {}

    fetch_page = (url, callback=null, foreground=true)->
      if url not of pages
        if foreground
          $entries_ct.addClass("loading")
        $.getJSON(url, (data)->
          pages[url] = data
          if foreground
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
      )

    $links.click((e)=>
      e.preventDefault()
      $target = $(e.target)
      if $target.is("span")
        $target = $target.parent()
      next = $target.hasClass("next")
      $entries_ct.effect("drop", {direction: if next then "left" else "right"}, ->
        $entries_ct.show()
        $entries_ct.empty()
        History.pushState({next: next}, null, $target.attr("href"))
      )
    )

    History.Adapter.bind(window, "statechange", =>
      state = History.getState()
      url = state.url
      next = state.data.next
      show_page(url, next)
    )

    prefetch_pages()


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
  preview_enabled = null
  text_changed = false

  $text.keyup((e)->
    text_changed = true
  )

  update_preview = ->
    if not preview_enabled
      return
    if text_changed
      text_changed = false
      $preview_area.html(markdown.toHTML($text.val()))
    setTimeout(update_preview, 100)

  enable_preview = ->
    preview_enabled = true
    $preview_area.fadeIn()
    update_preview()

  disable_preview = ->
    preview_enabled = false
    $preview_area.fadeOut()

  $preview_checkbox = $form.find("#id_preview")

  $preview_checkbox.change((e)->
    $this = $(this)
    if $this.attr("checked")
      enable_preview()
    else
      disable_preview()
  )

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
            $(response.comment).appendTo($comments).fadeIn()
          $form.detach().insertAfter($comments.find("article.comment").last())
        $buttons_ct.removeClass("loading")
        $submit_btn.removeAttr("disabled")
      )
    errorPlacement: (error, element)->
      error.appendTo(element.parents(".field").find(".errors"))
  )

