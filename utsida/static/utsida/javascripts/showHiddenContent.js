var acc = document.getElementsByClassName("accordion");

for (var i = 0; i < acc.length; i++) {
    acc[i].onclick = function() {
        this.classList.toggle("active");
        this.parentNode.previousElementSibling.classList.toggle("show");
        if (this.classList.contains("glyphicon-chevron-down")) {
            this.className = "accordion glyphicon glyphicon-chevron-up";
        }
        else if (this.classList.contains("glyphicon-chevron-up")){
            this.className = "accordion glyphicon glyphicon-chevron-down";
        }
    }
}

