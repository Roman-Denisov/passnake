$(document).ready(function () {
    let arr_num = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    let arr_en = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    let arr_symb = ['!', '@', '#', '$', '%', '?', '-', '+', '=', '~'];

    const compareRandom = ( ) => Math.random() - 0.5;
    const randomInteger = ( min, max ) => Math.round(min - 0.5 + Math.random() * (max - min + 1));
    const inputPassword = $('#modal-input-password');

    function generatePassword() {
        var id = $(this).attr('id');
        var postfix = '';
        if(id == 'pass_start_add')  {
            postfix = '_add';
        }

        let arr = [];
        var checked = false;
        if ($('#arr_num' + postfix).is(':checked')) {
            checked = true;
            arr = arr.concat(arr_num);
        }
        if ($('#arr_en' + postfix).is(':checked')){
            checked = true;
            arr = arr.concat(arr_en);
        }
        if ($('#arr_symb' + postfix).is(':checked'))  {
            checked = true;
            arr = arr.concat(arr_symb);
        }

        if(!checked) {
            alert('Не выбрано ни одного символа для составления пароля');
            return;
        }

        arr.sort(compareRandom);

        let password = '';
        let passLenght = $('#pass_lenght' + postfix).val();

        for (let i = 0; i < passLenght; i++) {
            password += arr[randomInteger(0, arr.length - 1)];
        }

        if(id == 'pass_start_add')  {
            $('#password').val(password);
        } else {
            inputPassword.val(password);
        }
    }

    $('.button-pass-start').on('click', generatePassword);

});