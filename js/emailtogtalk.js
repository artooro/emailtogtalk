$(function () {
    $('#btn_start').click(function () {
        $('#info_form').removeClass('hide');
        $('#info_form').html('Processing your request...');

        console.log('Subscribe form submitted.');
        $.ajax({
            url: '/app/subscribe',
            data: {
                'email': $('#email').val()
            },
            dataType: 'text',
            success: function (data) {
                console.log('Returned ' + data);
                if (data == 'EXISTS') {
                    $('#info_form').html('You are already subscribed. <a class="btn" href="/app/retrieve">email me my information</a>');
                    return true;
                }
                if (data == 'INVALID') {
                    $('#info_form').html('Please enter a valid email address.');
                    return true;
                }

                $('#info_form').html('Forward your emails to ' + data);
                $('#email').val('');

            }
        });

        return false;
    });

    $(document).on('click', 'a[href="/app/retrieve"]', function () {
        $('#info_form').removeClass('hide');
        $('#info_form').html('Processing your request...');

        console.log('Retrieving lost account info');

        $.ajax({
            url: '/app/retrieve',
            data: {
                'email': $('#email').val()
            },
            dataType: 'text',
            success: function (data) {
                $('#info_form').html("We've emailed you your account information.");
                $('#email').val('');
            }
        });

        return false;
    });
});