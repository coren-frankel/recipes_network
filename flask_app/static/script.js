function concealPassword() {
    var x = document.getElementById("pword");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}
function concealConfirm() {
    var y = document.getElementById("cword");
    if (y.type === "password") {
        y.type = "text";
    } else {
        y.type = "password";
    }
}
function concealPwordLog() {
    var z = document.getElementById("pwlog");
    if (z.type === "password") {
        z.type = "text";
    } else {
        z.type = "password";
    }
}