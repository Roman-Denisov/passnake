!function(e){"function"!=typeof e.matches&&(e.matches=e.msMatchesSelector||e.mozMatchesSelector||e.webkitMatchesSelector||function(e){for(var t=this,o=(t.document||t.ownerDocument).querySelectorAll(e),n=0;o[n]&&o[n]!==t;)++n;return Boolean(o[n])}),"function"!=typeof e.closest&&(e.closest=function(e){for(var t=this;t&&1===t.nodeType;){if(t.matches(e))return t;t=t.parentNode}return null})}(window.Element.prototype);
document.addEventListener("DOMContentLoaded", () => {

    const btn = document.getElementsByClassName('openmodel')
    const inputShareID = document.getElementById('modal-input-shareIDDesc')
    const inputId = document.getElementById('modal-input-id')
    const inputLogin = document.getElementById('modal-input-login')
    const inputUrl = document.getElementById('modal-input-url')
    const inputName = document.getElementById('modal-input-name')
    const inputPassword = document.getElementById('modal-input-password')
    const inputDefinition = document.getElementById('modal-input-definition')
    const inputTags = document.getElementById('modal-input-tags')
    const modal = document.getElementsByClassName('modal_normal')[0]
    const overlay = document.querySelector('.js-overlay-modal')

    for (var i = 0 ; i < btn.length; i++) {
        btn[i].addEventListener('click' , onClickBtnModal)
    };

    function onClickBtnModal () {
        overlay.classList.add('active');
        modal.classList.add('active')
        const val = JSON.parse(this.dataset.params);

        let password = getPassFromDB(val.inputIdValue);

        inputId.value = val.inputIdValue
        inputLogin.value = val.inputLoginValue
        inputUrl.value = val.inputUrlValue
        inputName.value = val.inputNameValue
        inputPassword.value = password
        inputPassword.setAttribute( "onClick", "getPass(this,"+val.inputIdValue+")" );
        inputDefinition.value = val.inputDefinitionValue
        inputTags.value = val.inputTagsValue
        inputShareID.value = val.inputShareIDValue
        inputId.value = val.inputIdValue
    }

    overlay.addEventListener('click', function() {
        modal.classList.remove('active');
        this.classList.remove('active');
        $('#selector').val(null).trigger('change');
    });

    document.body.addEventListener('keyup', function (e) {
        var key = e.keyCode;

        if (key == 27) {

            modal.classList.remove('active');
            overlay.classList.remove('active');
            $('#selector').val(null).trigger('change');
        };
    }, false);

    closeButtons = document.querySelectorAll('.js-modal-close');

    closeButtons.forEach(function(item) {
        item.addEventListener('click', function(e) {
            var parentModal = this.closest('.modal_normal');
            parentModal.classList.remove('active');
            overlay.classList.remove('active');
            $('#selector').val(null).trigger('change');
        });
    });
});
