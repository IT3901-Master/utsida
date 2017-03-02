/*
 Logic for adding new form fields when they are appropriate to appear in /process.
 */


var filterCountries = function () {
    var selectedContinent = $("#continentField").find(":selected").text();
    var countryRow = document.getElementById("countryRow");
    var countrySelectBox = document.getElementById("countryField");

    var clearSelectBox = function () {
        for (var i = countrySelectBox.options.length - 1; i >= 0; i--) {
            countrySelectBox.remove(i)
        }
    };

    if (selectedContinent != "---------") {

        countryRow.style.display = "block";
        clearSelectBox();

        $.post("/api/countries/", {'continent': selectedContinent})
            .done(function (data) {

                var placeholder = document.createElement('option');
                placeholder.value = "";
                placeholder.innerHTML = "---------";
                placeholder.setAttribute("selected", "True");
                countrySelectBox.appendChild(placeholder);

                data.forEach(function (country) {
                    var country_option = document.createElement("option");
                    country_option.textContent = country.pk;
                    countrySelectBox.appendChild(country_option)
                });
            });
    }
};
