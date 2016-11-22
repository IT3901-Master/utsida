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
        //this.removeMessage();
    },

    removeMessage: function() {
        setTimeout(function() {
            s.container.removeChild(s.container.firstChild);
            s.container.className = "hiddenDiv";
        }, 5000)
    }
};

