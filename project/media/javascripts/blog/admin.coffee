

class BlogAdmin

  constructor:(preview_url, @list_entry_images_url=null, @delete_image_url=null) ->
  
    settings = htmlSettings

    settings.previewParserPath = preview_url
    settings.previewInWindow = "width=800, height=600, resizable=yes, scrollbars=yes"
        
    oembed =
      name: "oembed"
      className: "oembed"
      openWith: "{% oembed %}"
      closeWith:"{% endoembed %}"

    highlight =
      name: "highlight"
      className: "codeButton"
      openWith: "{% highlight [![Syntax]!] %}"
      closeWith: "{% endhighlight %}"

    settings.markupSet.splice(18, 0, oembed, highlight)

    $("#id_text").markItUp(settings)

    datepicker_options =
      dateFormat: "dd.mm.yy"
      showButtonPanel: true
      changeMonth: true
      changeYear: true

    $("input.date").datepicker(datepicker_options)

    @form = $("#entry-form")

    @IMAGE_WIDGET_TEMPLATE = $.template(null,
     '''<li class="image" id="image-${id}" data-id="${id}" data-filename="${filename}">
          <span><img src="${src}" /></span>
          <a class="original" href="#"></a>
          <a class="scaled" href="#"></a>
          <a class="thumb" href="#"></a>
          <a class="delete" href="#"></a></li>''')

    @images_widget = $("#images-widget")
    @images_widget_container = @images_widget.find("ul.images");
    if @list_entry_images_url?
      $.getJSON(@list_entry_images_url, (data)=>
        for image in data.images
          $.tmpl(@IMAGE_WIDGET_TEMPLATE, image).appendTo(@images_widget_container)
        return
      )

    image_field =$("#id_images")

    @delete_image_confirmation = $("<div><img /></div>").appendTo($("body")).dialog(
      title: gettext("Delete this image?"),
      resizable: false,
      modal: true,
      autoOpen: false,
      buttons: [
        {
          text: gettext("Cancel"),
          click: ->
            $(@).dialog("close")
        },
        {
          text: gettext("Delete"),
          click: =>
            $dialog = @delete_image_confirmation
            $dialog.dialog("close");
            id = "" + $dialog.data("id")
            if not id
              return
            ids = image_field.val().split(",")
            image_field.val((_id for _id in ids when _id != id).join(","))
            $("#image-#{id}").fadeOut(300, ->
              $(@).remove()
            )
            $.post(@delete_image_url, {id: id}, ->)
        }
      ]
    )
    @delete_image_confirmation_img = @delete_image_confirmation.dialog("widget").find("img")

    @images_widget_container.delegate("a", "click", (e)=>
      e.preventDefault()
      $button = $(e.target)
      $image = $button.closest("li");
      id = $image.data("id")
      filename = $image.data("filename")
      button_cls = $button.attr("class")

      if button_cls == "delete"
        @delete_image_confirmation_img.attr("src", $image.find("img").attr("src"))
        @delete_image_confirmation.data("id", id)
        @delete_image_confirmation.dialog("open")
      else
        insert_text = "{% image #{id} #{button_cls} \"[![Alt:!:#{filename}]!]\" %}"
        $.markItUp(
          target: "#id_text",
          replaceWith: insert_text
        )
    )

    @upload_btn = $("#upload-image-button")
    @upload_btn.upload(
      action: @upload_btn.attr("href"),
      onComplete: (response)=>
        image = $.parseJSON(response).image
        $.tmpl(@IMAGE_WIDGET_TEMPLATE, image).appendTo(@images_widget_container)
        image_field.val(image_field.val() + ",#{image.id}")
    )

window.BlogAdmin = BlogAdmin