var button = document.getElementById("showHiddenContentBtn");
var allHiddenContent = document.getElementsByClassName("hidden");

var showHiddenContent = function() {

    for (var i = 0; i <= allHiddenContent.length; i++) {
        if (allHiddenContent[i].className == 'show') {
            allHiddenContent[i].className = 'hidden';
        }
        else if (allHiddenContent[i].className == 'hidden') {
            allHiddenContent[i].className = 'show';
        }

    }
};

button.addEventListener('click', function(e) {
    e.preventDefault();
    showHiddenContent();
});