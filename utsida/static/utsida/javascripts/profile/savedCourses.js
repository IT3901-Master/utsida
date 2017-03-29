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
            if ($('#courseList').children().length == 1) {
                $('#courseList').remove();
                $('#universityHeader').innerHTML = "Du har ikke lagret noen fag";
            }
        }
        else if (type == "course_match") {
            $.post("/profile/remove_course_match/", {'id': id});
            $('#courseMatchListModal').find("[data-id='" + id + "']").remove();
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
    $.ajax({
        url: "/profile/abroadCourse/add/",
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
            var mainDiv = document.createElement('div');
            mainDiv.setAttribute('data-university', json.university);
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

                var abroadUniversitySelect = document.createElement('select');
                abroadUniversitySelect.setAttribute("id","abroad_university_select");
                abroadUniversitySelect.append($("<option></option>")
                    .attr("value", json.university)
                    .text(json.university));

                var universityHeader = document.createElement('h4');
                universityHeader.innerHTML = "Lagrede fag ved " + abroadUniversitySelect;
                universityHeader.setAttribute("id", "universityHeader");
                $('#abroadCourseListContainer').prepend(universityHeader);


                $('#abroad_university_select').val(json.university);


            }
            $('#courseList').append(mainDiv);
            $('#add-abroad-course-form')[0].reset();

            refreshConfirmation();
            CourseMatcher.init();
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


function abroadCourseFilter() {
    var selected_uni = $('#abroad_university_select').val();
    var abroad_courses = $('#courseList').children();
    abroad_courses.filter(function () {
        return $(this).data("university") == selected_uni;
    }).show();
    abroad_courses.filter(function () {
        return $(this).data("university") != selected_uni;
    }).hide();
    CourseMatcher.clearAwayCourseSelection();
    $("#add-form-university option").filter(function () {
        return this.text == selected_uni;
    }).prop('selected', true);
}

$("#abroad_university_select").on('change', function () {
    abroadCourseFilter();
});


$('#add-course-form').on('submit', function (event) {
    event.preventDefault();
    var course = $('#id_coursesToTake').val();
    if (course.length < 6 || course.indexOf('-') == -1) {
        Messager.init();
        Messager.sendMessage('Velg et fag fra listen, feil input', "danger");
        return false;
    }
    var code = course.split(/-(.+)/)[0].trim();
    var name = course.split(/-(.+)/)[1].trim();

    $.ajax({
        url: "/profile/save_home_course/",
        type: "POST",
        data: {
            code: code,
            name: name
        },
        success: function (json) {
            Messager.init();
            CourseMatcher.toggleAddHomeCourse();
            Messager.sendMessage("Faget ble lagt til", "success");
            mainDiv = document.createElement('div');
            mainDiv.setAttribute('onclick', "CourseMatcher.markHomeCourse(this)");
            mainDiv.className = "centerCol courseBlock boxShadow pointer noSelect blockElement";
            mainDiv.innerHTML = "<span id='code'>" + json.code + "</span>" + ' - ' + "<span id='name'>" + json.name + "</span>";
            span2 = document.createElement('span');
            span2.setAttribute("data-toggle", "confirmation");
            span2.setAttribute("data-type", "home_course");
            span2.setAttribute("data-id", json.id);
            span2.className = "glyphicon glyphicon-remove pull-right pointer";
            mainDiv.append(span2);
            $('#homeCourseList').append(mainDiv);
            $('#id_coursesToTake').val('');
            refreshConfirmation();
            CourseMatcher.init();
        },
        error: function (err) {
            if (err.status == 409) {
                Messager.init();
                Messager.sendMessage("faget er allerede lagret!", "danger");
            }
            else if (err.status == 404) {
                Messager.init();
                Messager.sendMessage("Ugyldig fag, søk og velg fra listen!", "danger");
            }
        }
    })

});

function checkValidApplication() {
    if ($("#courseMatchList").children().size() == 0) {
        console.log("Empty course match list, not valid application");
        Messager.init();
        Messager.sendMessage("Du må ha fag i faglisten for å sende søknad", "danger")
    }
    else {
        $("#myModal").modal('show');
    }
};

abroadCourseFilter();



