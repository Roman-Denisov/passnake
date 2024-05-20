!function(e){"function"!=typeof e.matches&&(e.matches=e.msMatchesSelector||e.mozMatchesSelector||e.webkitMatchesSelector||function(e){for(var t=this,o=(t.document||t.ownerDocument).querySelectorAll(e),n=0;o[n]&&o[n]!==t;)++n;return Boolean(o[n])}),"function"!=typeof e.closest&&(e.closest=function(e){for(var t=this;t&&1===t.nodeType;){if(t.matches(e))return t;t=t.parentNode}return null})}(window.Element.prototype);
document.addEventListener("DOMContentLoaded", () => {

    const btn = document.getElementsByClassName('openmodelshare');
    const titleShare = document.getElementsByClassName('modal-title-share')[0];

    const inputID = document.getElementById('modal-input-shareID');
    const inputUser = document.getElementById('modal-input-shareUser');
    const modal = document.getElementsByClassName('modal_normal_share')[0];
    const inputSystem = document.getElementById('systemsShare');
    const overlay = document.querySelector('.js-overlay-modal');

    for (var i = 0 ; i < btn.length; i++) {
        btn[i].addEventListener('click' , onClickBtnModal);
    };

    function onClickBtnModal () {
        overlay.classList.add('active');
        modal.classList.add('active');
        const val = JSON.parse(this.dataset.params);
        titleShare.textContent = val.title;
        inputID.value = val.inputIDValue;
    }

    overlay.addEventListener('click', function() {
        modal.classList.remove('active');
        this.classList.remove('active');
    });

    document.body.addEventListener('keyup', function (e) {
        var key = e.keyCode;
        if (key == 27) {
            modal.classList.remove('active');
            overlay.classList.remove('active');
        };
    }, false);

    closeButtons = document.querySelectorAll('.js-modal-close');
    closeButtons.forEach(function(item) {
        item.addEventListener('click', function(e) {
            var parentModal = this.closest('.modal_normal_share');
            parentModal.classList.remove('active');
            overlay.classList.remove('active');
        });
    });

});


