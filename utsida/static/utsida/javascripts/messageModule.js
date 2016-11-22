/*
Module for sending frontend messages on the screen.
Can be used anywhere by calling Messager.init() followed by Messager.sendMessage('message', 'color of alert')
 */

Messager = {

    s: {
        container: null
    },

    init: function() {
        s.container = document.getElementById("messageContainer");
    },

    sendMessage: function(message, type) {
        s.container.className = "alert alert-" + type;
        if (s.container.firstChild)
            s.container.removeChild(s.container.firstChild);
        s.container.appendChild(document.createTextNode(message));
        s.container.addEventListener('click', function(e) {
            e.preventDefault();
            s.container.className = "hiddenDiv";
        });
    }
};

