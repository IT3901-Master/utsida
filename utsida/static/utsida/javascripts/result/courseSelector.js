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
        selectedCourseContainer: document.getElementById("selectedCourseContainer")
    },

    init: function() {
        s = this.settings;
    },

    addCourse: function(c) {
        var uni = c.parentNode.parentNode.previousSibling.previousSibling.innerText.split('(').slice()[0].slice(0, -1);
        var country = c.parentNode.parentNode.previousSibling.previousSibling.innerText.split('(').slice()[1].split(')')[0];
        var course = c.innerHTML;
        var splitCourse = course.split(' ');
        var code = splitCourse.shift();
        var name = splitCourse.join(' ');

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
    },

    saveCourses: function() {
        $.post("/profile/save_courses/", {'courses': JSON.stringify(s.selectedCourses)});
    }
};

courseContainerDrag = {
    settings: {
        selected: null,
        xPos: 0,
        yPos: 0,
        xElem: 0,
        yElem: 0,
        handle: document.getElementById("selectedCourseContainer")
    },

    init: function() {
        v = this.settings;
        document.onmousemove = this.moveElement;
        document.onmouseup = this.destroy;
        v.handle.onmousedown = function() {
            courseContainerDrag.initDrag(this);
            return false;
        }
    },

    initDrag: function(elem) {
        v.selected = elem;
        v.xElem = v.xPos - v.selected.offsetLeft;
        v.yElem = v.yPos - v.selected.offsetTop;
    },

    destroy: function() {
        v.selected = null;
    },

    moveElement: function(e) {
        v.xPos = document.all ? window.event.clientX : e.pageX;
        v.yPos = document.all ? window.event.clientY : e.pageY;
        if (v.selected !== null) {
            v.selected.style.left = (v.xPos - v.xElem) + 'px';
            v.selected.style.top = (v.yPos - v.yElem) + 'px';
        }
    }
};

courseSelector.init();
courseContainerDrag.init();
