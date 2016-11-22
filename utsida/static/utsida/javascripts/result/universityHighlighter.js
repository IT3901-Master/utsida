/*
Module which ensures that a selected university is highlighted in /results.
 */

var s;
universityHighlighter = {

    settings: {
        url: decodeURI(window.location.href.split('/').slice(-2)[0]),
        buttons: document.getElementsByTagName("button")
    },

    init: function() {
        s = this.settings;
        this.highlight();
    },

    highlight: function() {
        for (var i = 0; i < s.buttons.length; i++) {
            if (s.buttons[i].innerHTML.toLowerCase() == s.url.toLowerCase()) {
                s.buttons[i].style.backgroundColor = "#5cb85c";
                s.buttons[i].style.color = "#FFF";
            }
        }
    }
};

universityHighlighter.init();