var s;
courseSelector = {

    settings: {
        selectedCourses: [],
        numSelectedCourses: 0,
        selectedCourseBody: document.getElementById("selectedCourseBody"),
        selectedCourseToggleBtn: document.getElementById("selectedCourseToggleBtn"),
        numSelectedCoursesBadge: document.getElementById("numSelectedCoursesBadge"),
        selectedCourseFooter: document.getElementById("selectedCourseFooter"),
        selectedCourseList: document.getElementById("selectedCourseList"),
        selectedCourseContainer: document.getElementById("selectedCourseContainer")
    },

    init: function() {
        s = this.settings;
    },

    addCourse: function(course) {
        this.showContainer();
        if (!(s.selectedCourses.indexOf(course) > -1)) {
            s.selectedCourses.push(course);
            var label = document.createElement("li");
            label.innerHTML = course;
            s.selectedCourseList.appendChild(label);
            s.numSelectedCourses += 1;
            this.updateNumSelectedCourses();
        }
    },

    removeAllSelectedCourses: function() {
        s.selectedCourses = [];
        s.numSelectedCourses = 0;
        this.updateNumSelectedCourses();
        while(s.selectedCourseList.firstChild) {
            s.selectedCourseList.removeChild(s.selectedCourseList.firstChild)
        }
        this.toggleSelectedCourses();
        this.hideContainer();
    },

    updateNumSelectedCourses: function() {
        s.numSelectedCoursesBadge.innerHTML = s.numSelectedCourses.toString();
    },

    toggleSelectedCourses: function() {
        s.selectedCourseBody.style.display = s.selectedCourseBody.style.display == "none" ? "block" : "none";
        s.selectedCourseToggleBtn.className = s.selectedCourseToggleBtn.className == "pull-right glyphicon glyphicon-chevron-down" ? "pull-right glyphicon glyphicon-chevron-up" : "pull-right glyphicon glyphicon-chevron-down";
        s.selectedCourseFooter.style.display = s.selectedCourseFooter.style.display == "none" ? "block" : "none";
    },

    hideContainer: function() {
        s.selectedCourseContainer.style.display = "none";
    },

    showContainer: function() {
        s.selectedCourseContainer.style.display = "block";
    }

};

courseSelector.init();

/* Drag and drop code */
var selected = null;
var xPos = 0;
var yPos = 0;
var xElem = 0;
var yElem = 0;

function init_drag(elem) {
    selected = elem;
    xElem = xPos - selected.offsetLeft;
    yElem = yPos - selected.offsetTop;
}
function _destroy() {
    selected = null;
}
function _move_elem(e) {
    xPos = document.all ? window.event.clientX : e.pageX;
    yPos = document.all ? window.event.clientY : e.pageY;
    if (selected !== null) {
        selected.style.left = (xPos - xElem) + 'px';
        selected.style.top = (yPos - yElem) + 'px';
    }
}
courseSelector.settings.selectedCourseContainer.onmousedown = function() {
    init_drag(this);
    return false;
};
document.onmousemove = _move_elem;
document.onmouseup = _destroy;
