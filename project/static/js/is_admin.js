$(document).ready(function() {
    $('.toggle-admin > .toggle').click(function() {
        var el = $(this).siblings('.status');
        var current_status = $(el).text();
        var user_id = $(this).siblings("input:hidden").val();
        var val;
        if (current_status === 'False'){
            $(el).text('True');
            val = 1;
        } else {
            $(el).text('False');
            val = 0;
        }

        $.ajax({
            url: '/user/'+user_id+'/edit',
            type: 'GET',
            data: {
                user: user_id,
                is_admin: val
            }
        });
    });

    $('.toggle-active > .toggle').click(function() {
        var el = $(this).siblings('.status');
        var current_status = $(el).text();
        var user_id = $(this).siblings("input:hidden").val();
        var val;
        if (current_status === 'False'){
            $(el).text('True');
            val = 1;
        } else {
            $(el).text('False');
            val = 0;
        }

        $.ajax({
            url: '/user/'+user_id+'/edit',
            type: 'GET',
            data: {
                user: user_id,
                is_active: val
            }
        });
    });

});
