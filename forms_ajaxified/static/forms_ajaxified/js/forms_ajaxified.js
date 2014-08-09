// jQuery plugin to load a form via ajax and turn it into a self-submitting
// form.
//
// Usage:
//
// $('[data-class="form_ajaxified"]').formsAjaxified();
//

(function( $ ) {
    function load_form($form, url) {
        // Sends initial GET request to load the form and inject it into the
        // DOM
        //
        $.get(url, function(data) {
            $form.html(data);
            register_handlers($form, url);
        })
    }

    function register_handlers($form, url) {
        // Loads change handlers for self-submitting forms
        //
        $form.find('input,select,textarea').off('change');
        $form.find('input,select,textarea').on('change', function() {
            if ($(this).attr('data-selfsubmitting-ignore')) {
                return;
            }
            var inputElementId = $(this).attr('id');
            submit_form($form, url, inputElementId);
        });

        $form.find('[type="submit"]').off('click');
        $form.find('[type="submit"]').on('click', function(event) {
            if ($(this).attr('data-selfsubmitting-ignore')) {
                return;
            }
            event.preventDefault();
            submit_form(url, $form);
        });
    }

    function submit_form($form, url, inputElementId) {
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
                } else {
                    console.log(data);
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
                load_form($form, url);
            } else {
                register_handlers($form, url);
            }

        });
    };
}( jQuery ));
