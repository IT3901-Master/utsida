var selectedCourses = [];
var numSelectedCourses = 0;
var selectedCourseBody = document.getElementById("selectedCourseBody");
var selectedCourseToggleBtn = document.getElementById("selectedCourseToggleBtn");
var numSelectedCoursesBadge = document.getElementById("numSelectedCoursesBadge");
var selectedCourseFooter = document.getElementById("selectedCourseFooter");
var selectedCourseList = document.getElementById("selectedCourseList");
var selectedCourseContainer = document.getElementById("selectedCourseContainer");

function addCourse(course) {
    showContainer();
    if (!(selectedCourses.indexOf(course) > -1)) {
        selectedCourses.push(course);
        var label = document.createElement("li");
        label.innerHTML = course;
        selectedCourseList.appendChild(label);
        numSelectedCourses += 1;
        updateNumSelectedCourses();
    }
}

function toggleSelectedCourses() {
    selectedCourseBody.style.display = selectedCourseBody.style.display == "none" ? "block" : "none";
    selectedCourseToggleBtn.className = selectedCourseToggleBtn.className == "pull-right glyphicon glyphicon-chevron-down" ? "pull-right glyphicon glyphicon-chevron-up" : "pull-right glyphicon glyphicon-chevron-down";
    selectedCourseFooter.style.display = selectedCourseFooter.style.display == "none" ? "block" : "none";
}

function removeAllSelectedCourses() {
    selectedCourses = [];
    numSelectedCourses = 0;
    updateNumSelectedCourses();
    while(selectedCourseList.firstChild) {
        selectedCourseList.removeChild(selectedCourseList.firstChild)
    }
    toggleSelectedCourses();
    hideContainer();
}

function updateNumSelectedCourses() {
    numSelectedCoursesBadge.innerHTML = numSelectedCourses.toString();
}

function hideContainer() {
    selectedCourseContainer.style.display = "none";
}
function showContainer() {
    selectedCourseContainer.style.display = "block";
}