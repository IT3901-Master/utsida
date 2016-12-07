// Logic for accordion functionality on the case results in /results.

var acc = document.getElementsByClassName("accordion");
var headers = document.getElementsByClassName("panel-heading square-corners");

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


// Uncomment to remove textwrapping on overflowing text in results panel headings
/*
for (var j = 0; j < headers.length; j++) {
    headers[j].addEventListener('mouseover', function(e) {
        e.preventDefault();
        this.children[0].style.width = "100%";
        this.children[1].style.display = "none";
    });

    headers[j].addEventListener('mouseout', function(e) {
        e.preventDefault();
        this.children[0].style.width = "80%";
        this.children[1].style.display = "inline-block";
    });
}
*/




