//documentation: http://bootstrap-confirmation.js.org/
$('[data-toggle=confirmation]').confirmation({
    rootSelector: '[data-toggle=confirmation]',
    onConfirm: function () {
        var here = this;
        var block = $(this).context.parentNode.parentNode.parentNode;
        var id = $(this)[0].dataset["id"];
        var type = $(this)[0].dataset["type"];
        $.post("/profile/remove_application/", {'id': id});
        $(this).closest('.courseBlock').fadeOut("slow", function (here) {
            block.parentNode.removeChild(block)
        });

    },
    title: "Sikker på at du vil slette?",
    btnOkLabel: "Ja",
    btnCancelLabel: "Nei",
    singleton: true,
    popout: true,
    placement: "right",
    container: "body"

});


$('[data-toggle=changeStatusConfirmation]').confirmation({
    rootSelector: '[data-toggle=changeStatusConfirmation]',
    onConfirm: function () {
        var block = $(this).context.parentNode.parentNode.parentNode;
        var id = $(this)[0].dataset["id"];
        var type = $(this)[0].dataset["type"];

        if (type == "approve") {
            $(this).closest('.courseBlock').removeClass("bg-neutral");
            $(this).closest('.courseBlock').addClass("bg-success");
        }
        else {
            $(this).closest('.courseBlock').removeClass("bg-success");
            $(this).closest('.courseBlock').removeClass("bg-neutral");
            $(this).closest('.courseBlock').addClass("bg-danger");
        }
    },
    btnOkLabel: "Ja",
    btnCancelLabel: "Nei",
    singleton: true,
    popout: true,
    placement: "right",
    container: "body"

});

