(function($) {

    var PLUGIN_NAME = "textareaPreview";

    var settings = {
        "container" : null,
        "containerClass": "preview",
        "updateInterval": 100,
        "preprocess": null,
        "enabled": true
    };

    var methods = {
        "init": function(options) {
            if (options) {
                options = $.extend({}, settings, options);
            } else {
                options = $.extend({}, settings);
            }
            var $textareas = this.each(function() {
                var $this = $(this);
                var data = $this.data(PLUGIN_NAME);
                if (!data) {
                    var $container = null;
                    if (options.container && $(options.container).length) {
                        $container = $(options.container);
                    } else {
                        $container = $("<div></div>").addClass(options.containerClass).insertAfter($this);
                    }
                    $this.data(PLUGIN_NAME, {
                        container: $container,
                        updateInterval: options.updateInterval,
                        preprocess: options.preprocess,
                        textChanged: false
                    });
                }
            });
            if (options.enabled) {
                methods["enable"].apply($textareas);
            }
            return $textareas;
        },
        "enable": function() {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data(PLUGIN_NAME);

                data.enabled = true;
                data.textChanged = true;
                $this.data(PLUGIN_NAME, data);

                $this.bind("keyup." + PLUGIN_NAME, function() {
                    var data = $this.data(PLUGIN_NAME, data);
                    data.textChanged = true;
                    $this.data(PLUGIN_NAME, data);
                });

                var update_preview = function() {
                    var data = $this.data(PLUGIN_NAME, data);
                    if (!data.enabled) {
                        return;
                    }
                    if (data.textChanged) {
                        var text = $this.val();
                        if (data.preprocess) {
                            text = data.preprocess(text);
                        }
                        data.container.html(text);
                        data.textChanged = false;
                        $this.data(PLUGIN_NAME, data);
                    }
                    setTimeout(update_preview, data.updateInterval);
                };

                data.container.show();

                update_preview();
            });
        },
        "disable": function() {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data(PLUGIN_NAME);

                data.enabled = false;
                $this.data(PLUGIN_NAME, data);

                $this.unbind("keyup." + PLUGIN_NAME);

                data.container.hide();
            });
        }
    };

    $.fn[PLUGIN_NAME] = function(method) {

        if (methods[method]) {
            return methods[ method ].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.' + PLUGIN_NAME);
        }

    };
})(jQuery);