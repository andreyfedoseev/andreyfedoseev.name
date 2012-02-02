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

    yaCounter = null
    for prop of window
      if prop.match(/^yaCounter/)
        yaCounter = window[prop]
    ga = window._gaq

    count_page_view = ->
      if yaCounter
        yaCounter.hit(window.location.href)
      if ga
        ga.push(["_trackPageview", window.location.href])

    $links = $("nav.pages a")
    $prev = $links.filter(".prev")
    $next = $links.filter(".next")

    $(document).keypress((e)->
      if e.which == 63234 and e.ctrlKey and $prev.css("display") != "none"
        $prev.click()
      if e.which == 63235 and e.ctrlKey and $next.css("display") != "none"
        $next.click()
    )

    window.init_fancybox()
    window.init_fotorama()

    $links.pjax("#content div.entries")

    $entries_ct = $("#content div.entries")

    spinner_ct = $("<div></div>", {id: "spinner"}).css({width: "1000px", height: "50px"}).hide().insertAfter($entries_ct)
    spinner = new Spinner({shadow: false, width: 4}).spin(spinner_ct.get(0))

    $entries_ct.bind("start.pjax", (e, xhr, options)->
      window.scrollTo(0, $entries_ct.offset().top - 10)
      if options.clickedElement
        next = options.clickedElement.hasClass("next")
      else
        next = false
      $entries_ct.effect("drop", {direction: if next then "left" else "right"})
      $("#spinner").show()
    )

    $entries_ct.bind("end.pjax", (e, xhr, options)->
      if options.clickedElement
        next = options.clickedElement.hasClass("next")
      else
        next = false
      $("#spinner").hide()
      $entries_ct.effect("drop", {mode: "show", direction: if next then "right" else "left"})
      count_page_view()
    )


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

window.init_share_buttons = ->
  $ ->
    $("article.entry div.share-icons").click(->
      $this = $(this)
      url = $this.data("url")
      title = $this.data("title")
      $toolbox = $("""
      <div class="addthis_toolbox addthis_default_style">
      <a class="addthis_button_facebook_like" fb:like:layout="button_count"></a>
      <a class="addthis_button_tweet"></a>
      <a class="addthis_button_google_plusone" g:plusone:size="medium"></a>
      <a class="addthis_counter addthis_pill_style"></a>
      </div>
      """)
      $this.replaceWith($toolbox)
      addthis.toolbox($toolbox.get(0), {url: url, title: title})
    )

window.init_fotorama = ->
  $ ->
    $(".fotorama").fotorama(
      width: 800
    )
