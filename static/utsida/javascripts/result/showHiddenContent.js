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


var savedCoursesContainer = document.getElementById("savedCoursesContainer");
var savedCoursesContainerBody = document.getElementById("savedCoursesContainerBody");
var savedCoursesContainerChevron = document.getElementById("savedCoursesContainerChevron");

var toggleSavedCoursesContainer = function() {
    savedCoursesContainer.style.width = savedCoursesContainer.style.width === "30%" ? "13%" : "30%";
    savedCoursesContainerBody.style.display = savedCoursesContainerBody.style.display === "block" ? "none" : "block";
    if (savedCoursesContainerChevron.className === "glyphicon glyphicon-chevron-down pull-right") {
        savedCoursesContainerChevron.className = "glyphicon glyphicon-chevron-up pull-right";
    }
    else if (savedCoursesContainerChevron.className === "glyphicon glyphicon-chevron-up pull-right"){
        savedCoursesContainerChevron.className = "glyphicon glyphicon-chevron-down pull-right";
    }
};


// Uncomment to remove textwrapping on overflowing text in results panel headings

for (var j = 0; j < headers.length; j++) {
    headers[j].addEventListener('mouseover', function(e) {
        e.preventDefault();
        this.children[0].style.whiteSpace = "normal";
    });

    headers[j].addEventListener('mouseout', function(e) {
        e.preventDefault();
        this.children[0].style.whiteSpace = "nowrap";
    });
}





