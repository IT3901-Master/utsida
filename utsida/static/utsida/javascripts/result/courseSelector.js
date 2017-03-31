/*
Module which handles the logic around adding and saving courses to the profile
 */

var s, v;
courseSelector = {

    settings: {
        selectedCourses: [],
        numSelectedCourses: 0,
        university: null,
        selectedCourseBody: document.getElementById("selectedCourseBody"),
        selectedCourseToggleBtn: document.getElementById("selectedCourseToggleBtn"),
        numSelectedCoursesBadge: document.getElementById("numSelectedCoursesBadge"),
        selectedCourseFooter: document.getElementById("selectedCourseFooter"),
        selectedCourseList: document.getElementById("selectedCourseList"),
        selectedCourseContainer: document.getElementById("selectedCourseContainer"),
    },

    init: function() {
        s = this.settings;
    },

    addCourse: function(c) {
        var uni = c.parentNode.parentNode.previousSibling.previousSibling.innerText.split('(').slice()[0].slice(0, -1);
        var country = c.parentNode.parentNode.previousSibling.previousSibling.innerText.split('(').slice()[1].split(')')[0];
        var course = c.innerHTML;
        var code = "";
        var name = "";

        function hasNumber(string) {
            return /\d/.test(string);
        }

        if (!hasNumber(course.split(' ').shift())) {
            code = "";
            name = course;
        }
        else {
            var splitCourse = course.split(' ');
            code = splitCourse.shift();
            name = splitCourse.join(' ');
        }

        if ((uni == s.university || s.university == null) && !(this.isCourseAlreadyAdded(name))) {
            s.university = uni;

            s.selectedCourses.push({
                'code': code,
                'name': name,
                'university': uni,
                'country': country
            });

            var label = document.createElement("li");
            label.innerHTML = course;
            s.selectedCourseList.appendChild(label);
            s.numSelectedCourses += 1;
            this.updateNumSelectedCourses();
            this.showContainer();
        }
    },

    isCourseAlreadyAdded: function(newCourse) {
        for (var i = 0; i < s.selectedCourses.length; i++) {
            if (newCourse == s.selectedCourses[i].name) {
                return true;
            }
        }
        return false;
    },

    removeAllSelectedCourses: function() {
        s.selectedCourses = [];
        s.numSelectedCourses = 0;
        this.updateNumSelectedCourses();
        while(s.selectedCourseList.firstChild) {
            s.selectedCourseList.removeChild(s.selectedCourseList.firstChild)
        }
        s.university = null;
        this.hideContainer();
    },

    updateNumSelectedCourses: function() {
        s.numSelectedCoursesBadge.innerHTML = s.numSelectedCourses.toString();
    },

    toggleSelectedCourses: function() {
        s.selectedCourseBody.style.display = s.selectedCourseBody.style.display == "none" ? "block" : "none";
        s.selectedCourseToggleBtn.className = s.selectedCourseToggleBtn.className == "pull-right glyphicon glyphicon-chevron-down" ? "pull-right glyphicon glyphicon-chevron-up" : "pull-right glyphicon glyphicon-chevron-down";
        s.selectedCourseFooter.style.display = s.selectedCourseFooter.style.display == "none" ? "block" : "none";
        s.selectedCourseContainer.style.width = s.selectedCourseContainer.style.width == "13%" ? "30%" : "13%";
    },

    hideContainer: function() {
        s.selectedCourseContainer.style.display = "none";
    },

    showContainer: function() {
        s.selectedCourseContainer.style.display = "block";
    },

    saveCourses: function() {
        $.post("/profile/save_courses/", {'courses': JSON.stringify(s.selectedCourses)})
            .success(function(res) {
                res = JSON.parse(res);
                Messager.init();
                if (res.error != undefined && res.error == "illegal course")
                    Messager.sendMessage(res.message, "danger");
                else if (res.code != undefined && res.code == 200)
                    Messager.sendMessage(res.message, "success");
            });
        this.removeAllSelectedCourses();
        this.hideContainer();
    },

    checkout: function() {
        window.location = "/profile/courses/";
    }

};

courseSelector.init();
