setTimeout(function () {
    $('#sucessAlert').fadeOut('slow');
}, 5000);


//documentation: http://bootstrap-confirmation.js.org/
$('[data-toggle=confirmation]').confirmation({
    rootSelector: '[data-toggle=confirmation]',
    onConfirm: function () {
        var block = $(this);
        var id = $(this)[0].dataset["id"];
        var type = $(this)[0].dataset["type"];
        $.post("/courseMatch/delete/", {'id': id}, function () {
            block.parents('tr').fadeOut("slow", function (block) {
                $('#example').DataTable().draw();
            });
        });

    },
    title: "Er du sikker på at du vil slette?",
    btnOkLabel: "Ja",
    btnCancelLabel: "Nei",
    singleton: true,
    popout: true,
    placement: "left"

});


var addCourseMatch = function (id) {
    $.ajax({
        data: {"id": id},
        type: "POST",
        url: "/profile/save_course_match_id/",
        success: function (response) {
            Messager.init();
            Messager.sendMessage("Faget ble lagret", "success");
        },
        error: function (error) {
            if (error.status == 409) {
                Messager.init();
                Messager.sendMessage("Koblingen er allerede i din profil!", "danger");
            }
            else if (error.status == 406) {
                Messager.init();
                Messager.sendMessage("Det finnes fag fra et annet universitet i din profil", "danger");
            }
        }
    });
};


var create_abroad_course = function create_post() {
    if ($('#id_university').length > 0) {
        var university = $('#id_university').find(":selected").text();
    }
    else {
        var university = $('#add-form-university').val();
    }
    $.ajax({
        url: "/abroadCourse/add/",
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
        },
        error: function (err) {
            $('#addAbroadModal').modal('hide');
            if (err.status == 409) {
                Messager.init();
                Messager.sendMessage("faget finnes allerede!", "danger");
            }
            else {
                Messager.init();
                Messager.sendMessage("Fikk ikke lagt til faget, prøv igjen", "danger")
            }
        }
    })
};

$('#add-abroad-course-form').on('submit', function (event) {
    //event.preventDefault();
    //create_abroad_course();
});
