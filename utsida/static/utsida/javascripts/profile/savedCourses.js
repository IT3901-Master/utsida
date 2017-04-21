/*
 Logic for handling the lists of saved courses in profile/courses.
 */

var removeCourse = function (block, code, university) {
    $.post("/profile/remove_course/", {'course': code, 'university': university});
    block.parentNode.removeChild(block);
};

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
        var block = $(this).context.parentNode.parentNode;
        var id = $(this)[0].dataset["id"];
        var type = $(this)[0].dataset["type"];
        var university = $(this).closest('div').data("university");
        if (type == "abroad_course") {
            block = $(this).context.parentNode.parentNode.parentNode;
            $.post("/profile/remove_course/", {'id': id});

            var data_list = [];
            $("div:data(university)").each(function () {
                if ($(this).data("university") == university) {
                    data_list.push(this)
                }
            });
            if (data_list.length == 1) {
                $('#abroad_university_select').find('option').each(function () {
                    if ($(this).val() == university) {
                        $(this).remove();
                    }
                });
            }

            $(this).closest('.blockElement').fadeOut("slow", function (here) {
                if ($(this).css('background-color') == "rgb(51, 122, 183)") {
                    CourseMatcher.clearAwayCourseSelection();
                }
                block.parentNode.removeChild(block);
                if ($('#courseList').children().length == 0) {
                    $('#courseList').remove();
                    $("#universityHeader").text("Universitet i utlandet");
                    $("#noAbroadCourseHeader").css('display', 'block');
                    $("#abroad_university_select").css('display', 'none');


                }
                else {
                    abroadCourseFilter();
                }
            });

        }
        else if (type == "course_match") {
            $.post("/profile/remove_course_match/", {'id': id});
            var university = $(this).closest('tr').data("university");
            $('#courseMatchListModal').find("[data-id='" + id + "']").remove();


            $(this).closest('tr').fadeOut("slow", function (here) {

                var data_list = [];
                $("tr:data(university)").each(function () {
                    if ($(this).data("university") == university) {
                        data_list.push(this)
                    }
                });

                if (data_list.length == 1) {
                    $('#course_match_university_select').find('option').each(function () {
                        if ($(this).val() == university) {
                            $(this).remove();
                        }
                    });
                }
                $(this).closest("tr").remove();

                if ($('#courseMatchList').children().length == 0) {

                    $('#course_match_university_select').css('display', 'none');
                    $('#course_match_list_header').css('display', 'block');
                    $('#create_application_btn').css('display', 'none');
                }
                else {
                    courseMatchFilter();
                }
            });
        }
        else if (type == "home_course") {
            block = $(this).context.parentNode;
            $.post("/profile/remove_home_course/", {'id': id});
            $(this).closest('.blockElement').fadeOut("slow", function (here) {
                block.remove();
                if ($('#homeCourseList').children().length == 0) {
                    $("#emptyHomeCourseInfo").css('display', 'block');
                }
                if ($(this).css('background-color') == "rgb(51, 122, 183)") {
                    //CourseMatcher.clearHomeCourseSelection();
                }
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

function add_abroad_course() {
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
            var row = document.createElement('div');
            row.setAttribute("class","row");
            var col10 = document.createElement('div');
            col10.setAttribute("class","col-md-10");
            var col2 = document.createElement('div');
            col2.setAttribute("class","col-md-2");
            col10.innerHTML = "<span id='code'>" + json.code + "</span>" + ' - ' + "<span id='name'>" + json.name + "</span>";
            var editspan = document.createElement('span');
            editspan.setAttribute('class','glyphicon glyphicon-edit col-md-1 pointer');
            editspan.setAttribute('id','editAbroadCourse');
            editspan.setAttribute('onclick','location.href="/abroadCourse/edit/' + json.id + '/"');
            var span2 = document.createElement('span');
            span2.setAttribute("data-toggle", "confirmation");
            span2.setAttribute("data-type", "abroad_course");
            span2.setAttribute("data-id", json.id);
            span2.className = "glyphicon glyphicon-remove pull-right pointer";
            col2.append(span2);
            col2.append(editspan);
            row.append(col10);
            row.append(col2);
            mainDiv.append(row);


            //Check if no courses had been added before
            if ($('#courseList').length == 0) {
                $("#abroad_university_select").css('display', 'block');
                var option = document.createElement("option");
                option.innerText = json.university;
                $("#abroad_university_select").prepend(option);
                $('#abroad_university_select').val(json.university);
                $("#abroad_university_select").on('change', function () {
                    abroadCourseFilter();
                });
                $("#noAbroadCourseHeader").css('display', 'none');
                $("#universityHeader").text($("#abroad_university_select").find(':selected').text())


                var courseList = document.createElement('div');
                courseList.setAttribute("id", "courseList");
                $('#abroadCourseListContainer').prepend(courseList);

            }
            else if ($("#abroad_university_select").find('option:contains(' + json.university + ')').length == 0) {
                var option = document.createElement("option");
                option.innerText = json.university;
                $("#abroad_university_select").append(option);
                $("#abroad_university_select").val(json.university);
            }
            $('#courseList').append(mainDiv);
            $('#add-abroad-course-form')[0].reset();
            abroadCourseFilter();
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
    add_abroad_course();
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
    if ($("#abroad_university_select").find(':selected').text() != "") {
        $("#universityHeader").text($("#abroad_university_select").find(':selected').text())
    }
}

function courseMatchFilter() {
    var selected_uni = $('#course_match_university_select').val();
    var course_matches = $('#courseMatchList').children();
    var course_matches_modal = $('#courseMatchListModal').children();

    course_matches.filter(function () {
        return $(this).data("university") == selected_uni;
    }).show();
    course_matches.filter(function () {
        return $(this).data("university") != selected_uni;
    }).hide();

    course_matches_modal.filter(function () {
        return $(this).data("university") == selected_uni;
    }).show();
    course_matches_modal.filter(function () {
        return $(this).data("university") != selected_uni;
    }).hide();

    $("#courseMatchAwayTitle").text($("#course_match_university_select").find(':selected').text());


}

$("#course_match_university_select").on('change', function () {
    courseMatchFilter();
});

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
            $("#emptyHomeCourseInfo").css('display', 'none');
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
        Messager.init();
        Messager.sendMessage("Du må ha fag i faglisten for å sende søknad", "danger")
    }
    else {
        $("#myModal").modal('show');
    }
};

abroadCourseFilter();
courseMatchFilter();



