var idleTime = 0;
$(document).ready(function () {
    // Increment the idle time counter every minute.
    var idleInterval = setInterval(timerIncrement, 60000); // 1 minute = 60000

    // Zero the idle timer on mouse movement.
    $(this).click(function (e) {
        idleTime = 0;
    });
    $(this).keypress(function (e) {
        idleTime = 0;
    });
});

function timerIncrement() {
    if (idleTime > 5) { // 5 minutes
        window.location.href = "/logout";
    }
    idleTime = idleTime + 1;
 }