/*
Module for sending frontend messages on the screen.
Can be used anywhere by calling Messager.init() followed by Messager.sendMessage('message', 'color of alert')
 */

var m;
Messager = {

    m: {
        container: null
    },

    init: function() {
        m = this.m;
        m.container = document.getElementById("messageContainer");
    },

    sendMessage: function(message, type) {
        m.container.className = "alert alert-" + type;
        if (m.container.firstChild)
            m.container.removeChild(s.container.firstChild);
        m.container.appendChild(document.createTextNode(message));
        m.container.addEventListener('click', function(e) {
            e.preventDefault();
            m.container.className = "hiddenDiv";
        });
    }

};

