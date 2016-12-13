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


$('#showAllApplications').click(function () {
    $('.courseBlock').show();
});

$('#showApproved').click(function () {
    var blocks = $('.courseBlock');
    for (var i = 0; i < blocks.length; i++) {
        if (blocks[i].classList.contains("bg-success")) {
            $(blocks[i]).show();
        }
        else if (blocks[i].classList.contains("bg-danger")) {
            $(blocks[i]).hide();
        }
        else if (blocks[i].classList.contains("bg-neutral")){
            $(blocks[i]).hide();
        }
    }
});

$('#showDisapproved').click(function () {
    var blocks = $('.courseBlock');
    for (var i = 0; i < blocks.length; i++) {
         if (blocks[i].classList.contains("bg-danger")) {
            $(blocks[i]).show();
        }
        else if (blocks[i].classList.contains("bg-success")) {
            $(blocks[i]).hide();
        }
        else if (blocks[i].classList.contains("bg-neutral")){
            $(blocks[i]).hide();
        }
    }
});

$('#showPending').click(function () {
    var blocks = $('.courseBlock');
    for (var i = 0; i < blocks.length; i++) {
        if (blocks[i].classList.contains("bg-neutral")){
            $(blocks[i]).show();
        }
        else if (blocks[i].classList.contains("bg-success")) {
            $(blocks[i]).hide();
        }
        else if (blocks[i].classList.contains("bg-danger")){
            $(blocks[i]).hide();
        }
    }
});





$('[data-toggle=changeStatusConfirmation]').confirmation({
    rootSelector: '[data-toggle=changeStatusConfirmation]',
    onConfirm: function () {
        var block = $(this).context.parentNode.parentNode.parentNode;
        var id = $(this)[0].dataset["id"];
        var type = $(this)[0].dataset["type"];
        var ref = $(this);

        if (type == "approve") {
            $.post("/profile/application/editstatus/", {'id': id, "type": type}, function () {
                ref.closest('.courseBlock').removeClass("bg-neutral");
                ref.closest('.courseBlock').removeClass("bg-danger");
                ref.closest('.courseBlock').addClass("bg-success");
                ref.parent().parent().siblings('.status')[0].innerText = "Godkjent"
            });
        }
        else {
            $.post("/profile/application/editstatus/", {'id': id, "type": type}, function () {
                ref.closest('.courseBlock').removeClass("bg-success");
                ref.closest('.courseBlock').removeClass("bg-neutral");
                ref.closest('.courseBlock').addClass("bg-danger");
                ref.parent().parent().siblings('.status')[0].innerText = "Ikke godkjent"
            });
        }
    },
    btnOkLabel: "Ja",
    btnCancelLabel: "Nei",
    singleton: true,
    popout: true,
    placement: "right",
    container: "body"

});

