

function sendApproval() {
    $.ajax({
        data: {"comment": $("#comment").val(),"university": $('#course_match_university_select').val()},
        type: "POST",
        url: "/profile/send_approval/",
        success: function (response) {
            $("#myModal").modal('hide');
            Messager.init();
            Messager.sendMessage("Søknaden er sendt til godkjenning","success");
            window.location = "#top-navbar";
        },
        error: function (e, x, r) {
            console.log(e);
        }
    });
}