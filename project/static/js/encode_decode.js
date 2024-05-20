function getPass(obj, index, history = false) {
    if(!$(obj).hasClass("edit-pass") && $(obj).val() == '') {
        $(obj).addClass("edit-pass");
        let pass = getPassFromDB(index, history);
        $(obj).val(pass).select();
        copyTextInput();
    }
}

$(document).ready(function () {

    $('.passtext').blur( function(){
        $(this).removeClass("edit-pass");
        $(this).val('');
    })

});

// получает пароль из БД
function getPassFromDB(index, history) {
    let res = '';
    $.ajax({
        url: '/get_pass',
        method: 'POST',
        dataType: 'text',
        async: false,
        data: {
            'index': index,
            'history': history
        },
        success: function(data) {
            res = data;
        },
        error: function() {
            alert('Ошибка при получении пароля. Повторите попытку.');
        }
    });
    return res;
}
