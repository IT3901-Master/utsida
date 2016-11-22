var removeCourse = function(block, code, university) {
    $.post("/profile/remove_course/", {'course': code, 'university': university});
    block.parentNode.removeChild(block);
};

var removeAllCourses = function() {
    $.post("/profile/remove_all_courses/");
    while (document.getElementById("courseList").firstChild)
        document.getElementById("courseList").removeChild(document.getElementById("courseList").firstChild);
    window.location = "/profile/courses/";
};
