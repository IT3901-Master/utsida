$("#continent_select").on('change', function () {

    $.post("/courseMatch/countrySelect/", {'continent': $(this).val()}, function (data) {
        //Creates new select with country when continent has been selected
        var formGroup = document.createElement('div');
        formGroup.setAttribute("class", "form-group");
        var select = document.createElement('select');
        select.setAttribute("id", "country_select");
        select.setAttribute("class", "form-control");
        select.setAttribute("name", "country");
        var placeholder = document.createElement('option');
        placeholder.value = "";
        placeholder.innerHTML = "-Velg land-";
        placeholder.setAttribute("selected", "True");
        placeholder.setAttribute("disabled", "True");
        select.append(placeholder);

        //Add each country to the select
        data.forEach(function (country) {
            var countryOption = document.createElement('option');
            countryOption.innerHTML = country;
            select.append(countryOption)

        });

        formGroup.append(select);
        $("#university_select_country").empty();
        $("#university_select_university").empty();
        $("#university_select_country").append(formGroup);
        $("#selectUniversityButton").prop("disabled", true);
        $("#selectUniversityButton").addClass("disabled");

    });

});


$('#university_select_country').on('change', 'select', function () {
    $.post("/courseMatch/universitySelect/", {'country': $(this).val()}, function (data) {
        //Creates new select of university when country has been selected
        var formGroup = document.createElement('div');
        formGroup.setAttribute("class", "form-group");
        var select = document.createElement('select');
        select.setAttribute("id", "university_select");
        select.setAttribute("class", "form-control");
        select.setAttribute("name", "university");
        var placeholder = document.createElement('option');
        placeholder.value = "";
        placeholder.innerHTML = "-Velg universitet-";
        placeholder.setAttribute("selected", "True");
        placeholder.setAttribute("disabled", "True");
        select.append(placeholder);

        //Add each university to the select
        data.forEach(function (university) {
            var universityOption = document.createElement('option');
            universityOption.innerHTML = university.name + ' (' + university.count + ')';
            select.append(universityOption)

        });
        formGroup.append(select);
        $("#university_select_university").empty();
        $("#university_select_university").append(formGroup);
        $("#selectUniversityButton").prop("disabled", true);
        $("#selectUniversityButton").addClass("disabled");
    });
});


$('#university_select_university').on('change', 'select', function () {
    //Actives the form submit button when a university has been selected
    $("#selectUniversityButton").prop("disabled", false);
    $("#selectUniversityButton").removeClass("disabled");
});