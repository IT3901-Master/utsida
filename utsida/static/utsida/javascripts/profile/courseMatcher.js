var s;
CourseMatcher = {

    s: {
        awayCourses: null,
        homeCourses: null,
        awayCourseSelected: false,
        homeCourseSelected: false,
        courseMatchesList: null,
        superVisorEmail: null
    },

    init: function() {
        s = this.s;
        s.awayCourses = document.getElementById("courseList").children;
        s.homeCourses = document.getElementById("homeCourseList").children;
        s.courseMatchesList = document.getElementById("courseMatches");
    },

    matchSelectedCourses: function() {
        var awayCourse = "";
        var homeCourse = "";
        for (var i = 0; i < s.awayCourses.length; i++) {
            if (s.awayCourses[i].children[0].style.backgroundColor == "rgb(51, 122, 183)") {
                awayCourse = s.awayCourses[i].children[0].innerText;
            }
        }

        for (var j = 0; j < s.homeCourses.length; j++) {
            if (s.homeCourses[j].children[0].style.backgroundColor == "rgb(51, 122, 183)") {
                homeCourse = s.homeCourses[j].children[0].innerText;
            }
        }

        var match = document.createElement("li");
        var labelAway = document.createElement("div");
        var labelHome = document.createElement("div");
        var arrow = document.createElement("span");
        arrow.style.paddingRight = "10px";
        arrow.style.paddingLeft = "10px";
        arrow.className = "glyphicon glyphicon-link";
        labelAway.className = "label label-default";
        labelHome.className = "label label-default";
        labelAway.innerHTML = awayCourse;
        labelHome.innerHTML = homeCourse;
        match.appendChild(labelAway);
        match.appendChild(arrow);
        match.appendChild(labelHome);
        s.courseMatchesList.appendChild(match);

    },

    markAwayCourse: function(block) {
        this.clearAwayCourseSelection();
        block.style.backgroundColor = "#337ab7";
        s.awayCourseSelected = true;
    },

    markHomeCourse: function(block) {
        if (s.awayCourseSelected) {
            this.clearHomeCourseSelection();
            block.style.backgroundColor = "#337ab7";
            s.homeCourseSelected = true;
        }
    },

    clearAwayCourseSelection: function() {
        for (var i = 0; i < s.awayCourses.length; i++) {
            s.awayCourses[i].children[0].style.backgroundColor = "#FFF";
        }
    },

    clearHomeCourseSelection: function() {
        for (var i = 0; i < s.homeCourses.length; i++) {
            s.homeCourses[i].children[0].style.backgroundColor = "#FFF";
        }
    },

    sendToSupervisor: function() {

    }
};

CourseMatcher.init();