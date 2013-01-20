window.init_login_box = ->
  $login_box = $("#login-box")
  $login_box.css({left: ($(document).width() - $login_box.width()) / 2})
  $login_box.data("initialized", false)
  $login_box.data("displayed", false)
  $(document).keydown((e)->
    # Ctrl + L
    if e.which == 76 and e.ctrlKey
      if not $login_box.data("initialized")
        $login_box.data("initialized", true)
        $login_box.addClass("loading")
        $login_box.load($login_box.data("load-from"), ()->
          $login_box.removeClass("loading")
          $form = $login_box.find("form")
          $form.find("input:first").focus()
          $username_field = $form.find("#id_username")
          $password_field = $form.find("#id_password")
          $form.submit((e)->
            e.preventDefault()
            $.post($form.attr("action"), $form.serialize(), (response)->
              if response.status == "error"
                $login_box.effect("bounce", {"direction": "left", "distance": 20}, 200, ->
                  if not $username_field.val()
                    $username_field.focus()
                  else
                    $password_field.focus()
                )
              else
                window.location.reload()
            )
          )
        )
      if $login_box.data("displayed")
        $login_box.data("displayed", false)
        $login_box.slideUp()
      else
        $login_box.data("displayed", true)
        $login_box.slideDown(->
          $login_box.find("input:first").focus()
        )

    if e.which == 27 and $login_box.data("displayed")
      $login_box.slideUp()
  )
