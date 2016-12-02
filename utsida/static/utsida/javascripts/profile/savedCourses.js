/*
Logic for handling the lists of saved courses in profile/courses.
 */

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

//documentation: http://bootstrap-confirmation.js.org/
$('[data-toggle=confirmation]').confirmation({
            rootSelector: '[data-toggle=confirmation]',
			onConfirm: function() {
                block = $(this).context.parentNode;
                var id = $(this)[0].dataset["id"];
                var type = $(this)[0].dataset["type"];
                if (type == "abroad_course"){
                    $.post("/profile/remove_course/", {'id': id});
                }
                else if (type == "course_match.js") {
                    $.post("/profile/remove_course_match/", {'id': id});
                }

                block.parentNode.removeChild(block);

            },
            title: "Er du sikker på at du vil slette?",
            btnOkLabel: "Ja",
            btnCancelLabel: "Nei",
            singleton: true,
            popout: true

		});
