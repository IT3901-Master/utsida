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
        $.post("/courseMatch/delete/", {'id': id},function () {
            $('#example').DataTable().row(block.parents('tr')).remove().draw();
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
    console.log(document.getElementById("messageContainer"));
            $.ajax({
            data: {"id":id},
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
            }
        });
};
