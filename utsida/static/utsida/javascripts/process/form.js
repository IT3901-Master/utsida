var formStep = function() {
    var selectedContinent = $("#continentField :selected").text();
    var countryRow = document.getElementById("countryRow");
    var selectedCountry = $("#countryField :selected").text();
    var languageRow = document.getElementById("languageRow");

    if (selectedContinent != "---------")
        countryRow.style.display = "block";
    if (selectedCountry != "---------")
        languageRow.style.display = "block";
};
