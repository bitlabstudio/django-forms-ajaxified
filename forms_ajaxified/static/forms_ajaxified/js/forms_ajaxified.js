// jQuery plugin to load a form via ajax and turn it into a self-submitting
// form.
//
// Usage:
//
// $('[data-class="form_ajaxified"]').formsAjaxified();
//

(function( $ ) {
    function load_form($form, url, options) {
        // Sends initial GET request to load the form and inject it into the
        // DOM
        //
        $.get(url, function(data) {
            $form.html(data);
            register_handlers($form, url, options);
        })
    }

    function register_handlers($form, url, options) {
        // Loads change handlers for self-submitting forms
        //
        $form.find('input,select,textarea').off('change');
        $form.find('input,select,textarea').on('change', function() {
            if ($(this).attr('data-selfsubmitting-ignore')) {
                return;
            }
            var inputElementId = $(this).attr('id');
            submit_form($form, url, inputElementId, options);
        });

        $form.find('[type="submit"]').off('click');
        $form.find('[type="submit"]').on('click', function(event) {
            if ($(this).attr('data-selfsubmitting-ignore')) {
                return;
            }
            event.preventDefault();
            submit_form($form, url, '', options);
        });
    }

    function submit_form($form, url, inputElementId, options) {
        // Submits the form and handles the returned JSON response
        //
        var data = $form.serialize();

        if (data === '') {
            data = 'trigger_element=' + inputElementId;
        } else {
            data += '&trigger_element=' + inputElementId;
        }

        $.post(
            url,
            data,
            function(data, textStatus, jqXHR) {
                if (jqXHR.status == 278) {
                    window.location.href = jqXHR.getResponseHeader("Location");
                    return
                }

                // remove markup manipulation from last submit
                $('.form-group').removeClass('has-error');
                $('.error-message').remove();
                $form.find('[data-class="form-non-field-errors"]').hide();

                if (data.success === 1) {
                    var $trigger_element = $('#' + data.trigger_element);
                    $trigger_element.addClass('success');
                    function remove_class() {
                        $trigger_element.removeClass('success');
                    }
                    window.setTimeout(remove_class, 500);
                    return
                }

                var error_fields = Object.keys(data.errors);
                for (var i = 0; i < error_fields.length; i++) {
                    var field = error_fields[i];
                    if (field === 'id___all__') {
                        var $non_field_errors = $form.find('[data-class="form-non-field-errors"]');
                        $non_field_errors.html(data.errors[field]);
                        $non_field_errors.show();
                    } else {
                        var $field = $('#' + field);
                        var $form_group = $field.closest('.form-group');
                        $form_group.addClass('has-error');
                        var $field_or_group = $field.closest('.input-group');
                        if ($field_or_group.length === 0) {
                            $field_or_group = $field;
                        }
                        $('<label class="control-label error-message" for="'+ $field.attr('id') +'">'+ data.errors[field] +'</label>').insertAfter($field_or_group);
                    }
                }
            }
        );
    }

    $.fn.formsAjaxified = function(options) {
        // Main function of the jQuery plugin
        //
        return this.each(function() {
            var $form = $(this);
            var url = $form.attr('action');
            if ($form.html() === '') {
                $form.html('Loading...');
                load_form($form, url, options);
            } else {
                register_handlers($form, url, options);
            }

        });
    };
}( jQuery ));
