/*
Module which handles the logic for creating course matches in /profile/courses.
 */

var s;
CourseMatcher = {

    s: {
        awayCourses: null,
        homeCourses: null,
        awayCourseSelected: false,
        homeCourseSelected: false,
        courseMatchesContainer: null,
        superVisorEmail: null,
        wrapper: null
    },

    init: function() {
        s = this.s;
        s.awayCourses = document.getElementById("courseList").children;
        s.homeCourses = document.getElementById("homeCourseList").children;
        s.courseMatchesContainer = document.getElementById("courseMatches");
        s.wrapper = document.getElementById("courseMatchesWrapper");
    },

    matchSelectedCourses: function() {
        s.wrapper.style.display = "block";
        var awayCourse = "";
        var homeCourse = "";
        for (var i = 0; i < s.awayCourses.length; i++) {
            if (s.awayCourses[i].style.backgroundColor == "rgb(51, 122, 183)") {
                awayCourse = s.awayCourses[i].innerText;
            }
        }

        for (var j = 0; j < s.homeCourses.length; j++) {
            if (s.homeCourses[j].style.backgroundColor == "rgb(51, 122, 183)") {
                homeCourse = s.homeCourses[j].innerText;
            }
        }

        var match = document.createElement("div");
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
        s.courseMatchesContainer.appendChild(match);

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
            s.awayCourses[i].style.backgroundColor = "#FFF";
        }
    },

    clearHomeCourseSelection: function() {
        for (var i = 0; i < s.homeCourses.length; i++) {
            s.homeCourses[i].style.backgroundColor = "#FFF";
        }
    }
};

CourseMatcher.init();