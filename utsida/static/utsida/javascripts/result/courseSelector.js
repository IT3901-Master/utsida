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
