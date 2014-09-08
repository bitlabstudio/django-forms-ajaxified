// jQuery plugin to load a form via AJAX and turn it into a self-submitting
// form.
//
// Usage:
//
// $('[data-class="form_ajaxified"]').formsAjaxified();
//
// Possible options:
//
// * default_loading_text - string representing the loading text that should
//   appear on a submit button when submitting. Default is `Submitting...`
//

(function( $ ) {
    function get_loading_text($submit_button, options) {
        var loading_text = $submit_button.attr('data-loading-text');
        if (!loading_text) {
            loading_text = options.default_loading_text;
        }
        if (!loading_text) {
            loading_text = 'Submitting...';
        }
        return loading_text;
    }

    function get_interval($element) {
        var interval = $element.attr('data-autosave-interval');
        if (!interval) {
            return 15000;
        }
        return interval;
    }

    function load_form($form, url, options) {
        // Sends initial GET request to load the form and inject it into the
        // DOM
        //
        $.get(url, function(data) {
            $form.html(data);
            register_handlers($form, url, options);
        })
    }

    function create_object($form, url, $wrapper, options) {
        var data = $form.serialize();
        $.post(url, data, function(data) {
            $wrapper.append(data);
            $new_form = $wrapper.find('[data-class="form_ajaxified"]').last();
            var form_url = $new_form.attr('action');
            load_form($new_form, form_url, options);
        })
    }

    function register_handlers($form, url, options) {
        // Registers change event handlers for self-submitting forms
        //
        $form.find('input,select,textarea').off('change');
        $form.find('input,select,textarea').on('change', function() {
            if ($(this).attr('data-selfsubmitting-ignore')) {
                return;
            }
            submit_form($form, url, $(this), options);
        });

        $form.find('[type="submit"]').off('click');
        $form.find('[type="submit"]').on('click', function(event) {
            if ($(this).attr('data-selfsubmitting-ignore')) {
                return;
            }
            event.preventDefault();
            submit_form($form, url, $(this), options);
        });

        $form.find('[data-autosave="1"]').each(function() {
            var intervalTimer = '';
            var interval = get_interval($(this));
            var $element = $(this);
            $form.on('focusin', $element, function() {
                clearInterval(intervalTimer);
                intervalTimer = setInterval(function() {
                   submit_form($form, url, $element, options);
                }, interval);
            });
            $form.on('focusout', $element, function() {
                clearInterval(intervalTimer);
            });
        });

        $('body').off('click', '[data-ajax-add-wrapper]');
        $('body').on('click', '[data-ajax-add-wrapper]', function(event) {
            event.preventDefault();
            var wrapper = $(this).attr('data-ajax-add-wrapper');
            var $wrapper = $(wrapper);
            var $form = $(this).closest('form');
            var url = $form.attr('action');
            create_object($form, url, $wrapper, options);
        });
    }

    function submit_form($form, url, $inputElement, options) {
        // Submits the form and handles the returned JSON response.
        //
        // Displays error messages next to the fields or a success indicator.
        //
        var data = $form.serialize();
        var inputElementId = $inputElement.attr('id');

        if (data === '') {
            data = 'trigger_element=' + inputElementId;
        } else {
            data += '&trigger_element=' + inputElementId;
        }

        var loading_text = get_loading_text($inputElement, options);
        var original_value = '';
        if ($inputElement.attr('type') === 'submit') {
            // Disable button to prevent multiple submits
            if ($inputElement.get(0).tagName === 'BUTTON') {
                original_value = $inputElement.text();
                $inputElement.text(loading_text);
            } else {
                original_value = $inputElement.val();
                $inputElement.val(loading_text);
            }
            $inputElement.prop('disabled', true)
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
                if ($inputElement.attr('type') === 'submit') {
                    // Enable button again
                    if ($inputElement.get(0).tagName === 'BUTTON') {
                        $inputElement.text(original_value);
                    } else {
                        $inputElement.val(original_value);
                    }
                    $inputElement.prop('disabled', false)
                }

                if (data.success === 1) {
                    var $trigger_element = $('#' + data.trigger_element);
                    var is_delete_form = $form.attr('data-ajax-delete-element');
                    if (is_delete_form) {
                        $(is_delete_form).remove();
                        $form.remove();
                    } else {
                        $trigger_element.addClass('success');
                        function remove_class() {
                            $trigger_element.removeClass('success');
                        }
                        window.setTimeout(remove_class, 500);
                    }
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
        // Main function for general forms plugin.
        //
        if (!options) {
            options = {};
        }
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
