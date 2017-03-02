/*
 Logic for handling the lists of saved courses in profile/courses.
 */

var removeCourse = function (block, code, university) {
    $.post("/profile/remove_course/", {'course': code, 'university': university});
    block.parentNode.removeChild(block);
};

var removeHomeCourse = function (course) {
    console.log(course)
}


var removeAllCourses = function () {
    $.post("/profile/remove_all_courses/");
    while (document.getElementById("courseList").firstChild)
        document.getElementById("courseList").removeChild(document.getElementById("courseList").firstChild);
    window.location = "/profile/courses/";
};


var confirmationSettings = {
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
            console.log($('#courseList').children().length);
            if ($('#courseList').children().length == 1) {
                $('#courseList').remove();
                $('#universityHeader').innerHTML = "Du har ikke lagret noen fag";
            }
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
};

function refreshConfirmation() {
    $(document).ajaxStop(function () {
        $(document).find('[data-toggle=confirmation]').confirmation(confirmationSettings);
    });
}

//documentation: http://bootstrap-confirmation.js.org/
$('[data-toggle=confirmation]').confirmation(confirmationSettings);

function create_post() {
    if ($('#id_university').length > 0) {
        var university = $('#id_university').find(":selected").text();
    }
    else {
        var university = $('#add-form-university').val();
    }
    $.ajax({
        url: "/profile/abroadCourse/add/",
        type: "POST",
        data: {
            code: $('#add-form-code').val(),
            name: $('#add-form-name').val(),
            url: $('#add-form-url').val(),
            university: university,
            study_points: $('#add-form-study-points').val()
        },
        success: function (json) {
            $('#addAbroadModal').modal('hide');
            Messager.init();
            Messager.sendMessage("Faget ble lagt til", "success");
            var mainDiv = document.createElement('div');
            mainDiv.setAttribute('onclick', "CourseMatcher.markAwayCourse(this)");
            mainDiv.className = "centerCol courseBlock boxShadow pointer noSelect blockElement";
            mainDiv.innerHTML = "<span id='code'>" + json.code + "</span>" + ' - ' + "<span id='name'>" + json.name + "</span>";
            var span2 = document.createElement('span');
            span2.setAttribute("data-toggle", "confirmation");
            span2.setAttribute("data-type", "abroad_course");
            span2.setAttribute("data-id", json.id);
            span2.className = "glyphicon glyphicon-remove pull-right pointer";
            mainDiv.append(span2);

            //Check if no courses had been added before
            if ($('#courseList').length == 0) {
                $('#noAbroadCourseHeader').remove();
                var courseList = document.createElement('div');
                courseList.setAttribute("id", "courseList");
                $('#abroadCourseListContainer').prepend(courseList);
                var universityHeader = document.createElement('h4');
                universityHeader.innerText = "Lagrede fag ved " + json.university + ', ' + json.country;
                universityHeader.setAttribute("id", "universityHeader");
                $('#abroadCourseListContainer').prepend(universityHeader);

                //Delete university selection from form and add hidden input
                $('#id_university').parent().remove();

                var hiddenUniversityInput = document.createElement('input');
                hiddenUniversityInput.setAttribute("type", "hidden");
                hiddenUniversityInput.setAttribute("id", "add-form-university");
                hiddenUniversityInput.setAttribute("name", "university");
                hiddenUniversityInput.setAttribute("value", json.university);
                $('#add-abroad-course-form .modal-body')[0].append(hiddenUniversityInput);
            }
            $('#courseList').append(mainDiv);
            $('#add-abroad-course-form')[0].reset();

            refreshConfirmation();
        },
        error: function (err) {
            $('#addAbroadModal').modal('hide');
            if (err.status == 409) {
                Messager.init();
                Messager.sendMessage("faget er allerede i din profil!", "danger");
            }
            else {
                Messager.init();
                Messager.sendMessage("Fikk ikke lagt til faget, prøv igjen", "danger")
            }
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
    var code = course.split(/-(.+)/)[0].replace(" ", "");
    var name = course.split(/-(.+)/)[1].replace(" ", "");
    $.ajax({
        url: "/profile/save_home_course/",
        type: "POST",
        data: {
            code: code,
            name: name
        },
        success: function (json) {

            Messager.init();
            if (json.error) {
                Messager.sendMessage(json.error, "danger");
            }
            else {
                Messager.sendMessage("Faget ble lagt til", "success");
                mainDiv = document.createElement('div');
                mainDiv.setAttribute('onclick', "CourseMatcher.markAwayCourse(this)");
                mainDiv.className = "centerCol courseBlock boxShadow pointer noSelect blockElement";
                mainDiv.innerHTML = "<span id='code'>" + json.code + "</span>" + ' - ' + "<span id='name'>" + json.name + "</span>";
                span2 = document.createElement('span');
                span2.setAttribute("data-toggle", "confirmation");
                span2.setAttribute("data-type", "home_course");
                span2.setAttribute("data-id", json.id);
                span2.className = "glyphicon glyphicon-remove pull-right pointer";
                mainDiv.append(span2);
                $('#homeCourseList').prepend(mainDiv);
                $('#id_coursesToTake').val('');
                refreshConfirmation();
            }
        },
        error: function (xhr, errmsg, err) {

        }
    })

});


