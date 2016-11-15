var highlight = function() {
    var url = decodeURI(window.location.href.split('/').slice(-2)[0]);
    var buttons = document.getElementsByTagName("button");

    for (var i = 0; i < buttons.length; i++) {
        if (buttons[i].innerHTML.toLowerCase() == url.toLowerCase()) {
            buttons[i].style.backgroundColor = "#5cb85c";
        }
        else if (buttons[i].innerHTML.toLowerCase() == url.toLowerCase() + 'e') {
            buttons[i].style.backgroundColor = "#5cb85c";
        }
    }
};

highlight();






