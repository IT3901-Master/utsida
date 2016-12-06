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

    init: function () {
        s = this.s;
        if (document.getElementById("courseList")) {
            s.awayCourses = document.getElementById("courseList").children;
        }
        else {
            s.awayCourses = [];
        }
        s.homeCourses = document.getElementById("homeCourseList").children;
        s.courseMatchesContainer = document.getElementById("courseMatches");
        s.wrapper = document.getElementById("courseMatchesWrapper");
        s.courseMatchList = {};
    }
    ,

    matchSelectedCourses: function () {
        var awayCourse = "";
        var homeCourse = "";
        for (var i = 0; i < s.awayCourses.length; i++) {
            if (s.awayCourses[i].style.backgroundColor == "rgb(51, 122, 183)") {
                awayCourse = s.awayCourses[i].innerText;
                var code = s.awayCourses[i].children[0].innerText;
                var name = s.awayCourses[i].children[1].innerText;
                s.courseMatchList["abroadCourseCode"] = code;
                s.courseMatchList["abroadCourseName"] = name;
            }
        }

        for (var j = 0; j < s.homeCourses.length; j++) {
            if (s.homeCourses[j].style.backgroundColor == "rgb(51, 122, 183)") {
                homeCourse = s.homeCourses[j].innerText;
                var code = s.homeCourses[j].children[0].innerText;
                var name = s.homeCourses[j].children[1].innerText;
                s.courseMatchList["homeCourseCode"] = code;
                s.courseMatchList["homeCourseName"] = name;
            }
        }
        $.ajax({
            data: s.courseMatchList,
            type: "POST",
            url: "/profile/save_course_match/",
            success: function (response) {
                var content = document.createElement("div");
                var abroadCourseSpan = document.createElement("span");
                abroadCourseSpan.className = "label label-default";
                abroadCourseSpan.innerText = s.courseMatchList["abroadCourseCode"] + " - " + s.courseMatchList["abroadCourseName"];

                var fillerSpan = document.createElement("span");
                fillerSpan.className = "glyphicon glyphicon-link";
                fillerSpan.style.paddingRight = "10px";
                fillerSpan.style.paddingLeft = "10px";

                var homeCourseSpan = document.createElement("span");
                homeCourseSpan.className = "label label-default";
                homeCourseSpan.innerText = s.courseMatchList["homeCourseCode"] + " - " + s.courseMatchList["homeCourseName"];

                content.appendChild(abroadCourseSpan);
                content.appendChild(fillerSpan);
                content.appendChild(homeCourseSpan);

                var content2 = content.cloneNode(true);
                document.getElementById("courseMatchList").appendChild(content);
                document.getElementById("courseMatchListModal").appendChild(content2);

                Messager.init();
                Messager.sendMessage("Faget ble lagret", "success");
            },
            error: function (error) {
                if (error.status == 409) {
                    Messager.init();
                    Messager.sendMessage("Koblingen er allerede i din profil!", "danger");
                }
            }
        });


    },

    markAwayCourse: function (block) {
        this.clearAwayCourseSelection();
        block.style.backgroundColor = "#337ab7";
        block.style.color = "white";
        s.awayCourseSelected = true;
    },

    markHomeCourse: function (block) {
        if (s.awayCourseSelected) {
            this.clearHomeCourseSelection();
            block.style.backgroundColor = "#337ab7";
            block.style.color = "white";
            s.homeCourseSelected = true;
        }
    },

    clearAwayCourseSelection: function () {
        for (var i = 0; i < s.awayCourses.length; i++) {
            s.awayCourses[i].style.backgroundColor = "#FFF";
            s.awayCourses[i].style.color = "black";
        }
    },

    clearHomeCourseSelection: function () {
        for (var i = 0; i < s.homeCourses.length; i++) {
            s.homeCourses[i].style.backgroundColor = "#FFF";
            s.homeCourses[i].style.color = "black";
        }
    }
};

CourseMatcher.init();