

class BlogAdmin

  constructor:(list_entry_images_url=null, upload_image_url=null, delete_image_url=null) ->

    datepicker_options =
      dateFormat: "dd.mm.yy"
      showButtonPanel: true
      changeMonth: true
      changeYear: true

    $("input.date").datepicker(datepicker_options)

    $form = $("#entry-form")
    $text = $("#id_text")
    $markdown_checkbox = $("#id_markdown")

    $preview_btn = $("#preview-button")
    
    $preview_form = $("<form>",
      action: $preview_btn.data("url"),
      target: "preview",
      method: "post"
    )

    $preview_text_input = $("<input>",
      type: "hidden",
      name: "text"
    ).appendTo($preview_form)

    $preview_markdown_input = $("<input>",
      type: "hidden",
      name: "markdown"
      value: "yes"
    ).appendTo($preview_form)

    $preview_form.appendTo($("body"))

    $preview_form.submit((e)->
      window.open("", "preview", "width=800,height=600,toolbar=no,location=no,status=no,menubar=no")
    )

    $preview_btn.click((e)->
      e.preventDefault()
      $preview_text_input.val($text.val())

      if $markdown_checkbox.attr("checked")
        $preview_markdown_input.removeAttr("disabled")
      else
        $preview_markdown_input.attr("disabled", "disabled")
      $preview_form.submit()
    )

    IMAGE_WIDGET_TEMPLATE = $.template(null,
     '''<li class="image" id="image-${id}" data-id="${id}" data-name="${name}">
          <span><img src="${src}" /></span>
          <a class="figure" href="#"></a>
          <a class="original" href="#"></a>
          <a class="scaled" href="#"></a>
          <a class="thumb" href="#"></a>
          <a class="delete" href="#"></a></li>''')

    $images_widget = $("#images-widget")
    $images_widget_container = $images_widget.find("ul.images");
    if list_entry_images_url?
      $.getJSON(list_entry_images_url, (data)=>
        for image in data.images
          $.tmpl(IMAGE_WIDGET_TEMPLATE, image).appendTo($images_widget_container)
        return
      )

    image_field =$("#id_images")

    delete_image_message = gettext("Delete this image?")

    $images_widget_container.delegate("a", "click", (e)=>
      e.preventDefault()
      $button = $(e.target)
      $image = $button.closest("li");
      id = $image.data("id")
      name = $image.data("name")
      button_cls = $button.attr("class")

      if button_cls == "delete"
        image_src = $image.find("img").attr("src")
        body = "<div>#{delete_image_message}</div><p class=\"align-center\"><img src=\"#{image_src}\" /></p>"
        apprise(body,
          verify: true,
          textYes: gettext("Yes"),
          textNo: gettext("No")
        (r)->
          if r
            id = "" + id
            ids = image_field.val().split(",")
            image_field.val((_id for _id in ids when _id != id).join(","))
            $("#image-#{id}").fadeOut(300, ->
              $(this).remove()
            )
            $.post(delete_image_url, {id: id}, ->)
        )
      else
        insert_text = "{% image #{id} #{button_cls} \"#{name}\" %}"
        $text.val($text.val() + insert_text)
    )

    $upload = $("#upload-image")
    $progressbar = $("#upload-image-progressbar").hide().progressbar()
    $upload.fileupload(
      url: upload_image_url,
      singleFileUploads: false,
#      fileInput: $form.find("input:file"),
      start: (e)->
        $progressbar.progressbar(
          value: 0
        )
        $progressbar.show()
      ,
      always: (e, data)->
        $progressbar.hide()
        response = data.result
        if response.status == "success"
          for image in response.images
            $.tmpl(IMAGE_WIDGET_TEMPLATE, image).appendTo($images_widget_container)
            image_field.val(image_field.val() + ",#{image.id}")
            console.log(image)
      ,
      progressall: (e, data)->
        $progressbar.progressbar(
          value: parseInt(data.loaded / data.total * 100, 10)
        )
    )

window.BlogAdmin = BlogAdmin