    var optionsCache = [];

function filterItems(el) {
  var value = el.value.toLowerCase();
  var form = el.form;
  var opt, sel = form.systemsShare;
  restoreOptions();
  for (var i=sel.options.length-1; i>=0; i--) {
    opt = sel.options[i];
    if (opt.text.toLowerCase().indexOf(value) == -1){
      opt.classList.add('hide');
    }
  }
}

function restoreOptions(){
  var sel = document.getElementById('systemsShare');
  for (var i=0, iLen=sel.length; i<iLen; i++) {
    opt = sel.options[i];
    opt.classList.remove('hide');
  }
}

window.onload = function() {
  var sel = document.getElementById('systemsShare');
  for (var i=0, iLen=sel.options.length; i<iLen; i++) {
    optionsCache.push(sel.options[i]);
  }
}