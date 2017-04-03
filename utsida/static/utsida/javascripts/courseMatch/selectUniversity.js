$("#continent_select").on('change', function () {

    var continent = $(this).val();
    $("#country_select")[0].selectedIndex = 0;
    $("#country_select").find("option").each(function () {
        if ($(this).data("continent") != undefined) {
            if ($(this).data("continent") == continent) {
                $(this).show();
            }
            else {
                $(this).hide();
            }
        }
    });
    $("#university_select").find("option").each(function () {
        if ($(this).data("continent") != undefined) {
            if ($(this).data("continent") == continent) {
                $(this).show();
            }
            else {
                $(this).hide();
            }
        }
    });
});


$('#university_select_country').on('change', 'select', function () {
    var country = $(this).val();
        $("#university_select").find("option").each(function () {
        if ($(this).data("country") != undefined) {
            if ($(this).data("country") == country) {
                $(this).show();
            }
            else {
                $(this).hide();
            }
        }
    });
});


$('#university_select_university').on('change', 'select', function () {
    //Actives the form submit button when a university has been selected
    $("#selectUniversityButton").prop("disabled", false);
    $("#selectUniversityButton").removeClass("disabled");
});