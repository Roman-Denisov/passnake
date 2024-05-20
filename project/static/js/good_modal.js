const btn = document.getElementsByClassName('openmodel')
const title = document.getElementsByClassName('modal-title')[0]
const input = document.getElementsByClassName('modal-input')[0]
const modal = document.getElementsByClassName('modal')[0]

for (var i = 0 ; i < btn.length; i++) {
   btn[i].addEventListener('click' , onClickBtnModal)
};

function onClickBtnModal () {
  modal.classList.add('active')
  const val = JSON.parse(this.dataset.params);
  console.log('А что это ты тут делоеш? /( о.о)/')
  title.textContent = val.title
  input.value = val.inputValue
}