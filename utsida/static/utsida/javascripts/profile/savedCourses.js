/*
 Logic for handling the lists of saved courses in profile/courses.
 */

var removeCourse = function (block, code, university) {
    $.post("/profile/remove_course/", {'course': code, 'university': university});
    block.parentNode.removeChild(block);
};

var removeHomeCourse = function(course) {
    console.log(course)
}


var removeAllCourses = function () {
    $.post("/profile/remove_all_courses/");
    while (document.getElementById("courseList").firstChild)
        document.getElementById("courseList").removeChild(document.getElementById("courseList").firstChild);
    window.location = "/profile/courses/";
};

var toggleAddHomeCourse = function() {
    var form = document.getElementById("add-course-form");
    form.style.display = form.style.display === 'block' ? 'none' : 'block';
};

//documentation: http://bootstrap-confirmation.js.org/
$('[data-toggle=confirmation]').confirmation({
    rootSelector: '[data-toggle=confirmation]',
    onConfirm: function () {
        var here = this;
        var block = $(this).context.parentNode;
        var id = $(this)[0].dataset["id"];
        var type = $(this)[0].dataset["type"];
        if (type == "abroad_course") {
            $.post("/profile/remove_course/", {'id': id});
            $(this).closest('.blockElement').fadeOut("slow", function (here) {
                block.parentNode.removeChild(block)
            });
        }
        else if (type == "course_match") {
            $.post("/profile/remove_course_match/", {'id': id});
            $(this).closest('tr').fadeOut("slow", function (here) {
                $(this).closest("tr").remove()
            });
        }
        else if (type == "home_course") {
            $.post("/profile/remove_home_course/", {'id': id});
            $(this).closest('.blockElement').fadeOut("slow", function (here) {
                block.parentNode.removeChild(block)
            });
        }


    },
    title: "Er du sikker på at du vil slette?",
    btnOkLabel: "Ja",
    btnCancelLabel: "Nei",
    singleton: true,
    popout: true

});

function create_post() {
    $.ajax({
        url: "/abroadCourse/add/",
        type: "POST",
        data: {
            code: $('#add-form-code').val(),
            name: $('#add-form-name').val(),
            url: $('#add-form-url').val(),
            university: $('#add-form-university').val(),
            study_points: $('#add-form-study-points').val()
        },
        success: function (json) {
            $('#addAbroadModal').modal('hide');
            Messager.init();
            Messager.sendMessage("Faget ble lagt til", "success");
            mainDiv = document.createElement('div');
            mainDiv.setAttribute('onclick', "CourseMatcher.markAwayCourse(this)");
            mainDiv.className = "centerCol courseBlock boxShadow pointer noSelect blockElement";
            mainDiv.innerHTML = "<span id='code'>" + json.code + "</span>" + ' - ' + "<span id='name'>" + json.name + "</span>";
            span2 = document.createElement('span');
            span2.setAttribute("data-toggle", "confirmation");
            span2.setAttribute("data-type", "abroad_course");
            span2.setAttribute("data-id", 1);
            span2.className = "glyphicon glyphicon-remove pull-right pointer";
            mainDiv.append(span2);
            $('#courseList').append(mainDiv);
            $('#add-abroad-course-form').reset();
        },
        error: function (xhr, errmsg, err) {
            $('#addAbroadModal').modal('hide');
            Messager.init();
            Messager.sendMessage("Fikk ikke lagt til faget, prøv igjen", "error")
        }
    })
}
$('#add-abroad-course-form').on('submit', function (event) {
    event.preventDefault();
    create_post();
});

$('#add-course-form').on('submit', function (event) {
    event.preventDefault();
    var course = $('#id_coursesToTake').val();
    var code = course.split(/-(.+)/)[0].replace(" ","");
    var name = course.split(/-(.+)/)[1].replace(" ","");
    $.ajax({
        url: "/profile/save_home_course/",
        type: "POST",
        data: {
            code: code,
            name: name
        },
        success: function (json) {
            console.log("YEEEEY, saved!!");
            Messager.init();
            Messager.sendMessage("Faget ble lagt til", "success");
            mainDiv = document.createElement('div');
            mainDiv.setAttribute('onclick', "CourseMatcher.markAwayCourse(this)");
            mainDiv.className = "centerCol courseBlock boxShadow pointer noSelect blockElement";
            mainDiv.innerHTML = "<span id='code'>" + json.code + "</span>" + ' - ' + "<span id='name'>" + json.name + "</span>";
            span2 = document.createElement('span');
            span2.setAttribute("data-toggle", "confirmation");
            span2.setAttribute("data-type", "abroad_course");
            span2.setAttribute("data-id", 1);
            span2.className = "glyphicon glyphicon-remove pull-right pointer";
            mainDiv.append(span2);
            $('#homeCourseList').append(mainDiv);
        },
        error: function (xhr, errmsg, err) {

        }
    })

});


