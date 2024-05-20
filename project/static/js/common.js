function copyTextInput() {
    document.execCommand("copy");

    new Noty({
       type: 'info',
       text: 'Скопировано в буфер обмена ✅',
       layout: 'topRight',
       theme: 'metroui',
       timeout: '200',
       progressBar: true,
       closeWith: ['click'],

     }).show();
}

function excludeRus(obj) {
    setTimeout(function() {
        obj.value = obj.value.replace(/([а-яА-ЯёЁ\s])/g, '');
    }, 0);
}

$(document).ready(function () {

    $('input').click( function(){
        $(this).select();
    })

    $('.passtextcopy').click( function(){
        $(this).select();
        copyTextInput();
    })

    $('#password').on('keypress', function() {
        excludeRus(this);
    });
    $('#password').on('paste', function() {
        excludeRus(this);
    });
    $('#modal-input-password').on('keypress', function() {
        excludeRus(this);
    });
    $('#modal-input-password').on('paste', function() {
        excludeRus(this);
    });
})