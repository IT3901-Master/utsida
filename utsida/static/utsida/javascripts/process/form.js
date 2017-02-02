/*
Logic for adding new form fields when they are appropriate to appear in /process.
 */

var formStep = function() {
    var selectedContinent = $("#continentField :selected").text();
    var countryRow = document.getElementById("countryRow");
    var countrySelectBox = document.getElementById("countrySelectBox");

    var clearSelectBox = function() {
        for (var i = countrySelectBox.options.length - 1; i >= 0; i--) {
            countrySelectBox.remove(i)
        }
    };

    if (selectedContinent != "---------") {

        countryRow.style.display = "block";
        clearSelectBox();

        if (selectedContinent === "Asia") {
            $.post("/api/countries/", {'continent': selectedContinent})
                .done(function(data) {
                    data.forEach(function(country) {
                        var country_option = document.createElement("option");
                        country_option.textContent = country.pk;
                        countrySelectBox.appendChild(country_option)
                    })
                });
        }
        else if (selectedContinent === "Europe") {
            $.post("/api/countries/", {'continent': selectedContinent})
                .done(function(data) {
                    data.forEach(function(country) {
                        var country_option = document.createElement("option");
                        country_option.textContent = country.pk;
                        countrySelectBox.appendChild(country_option)
                    })
                });
        }
        else if (selectedContinent === "Oceania") {
            $.post("/api/countries/", {'continent': selectedContinent})
                .done(function(data) {
                    data.forEach(function(country) {
                        var country_option = document.createElement("option");
                        country_option.textContent = country.pk;
                        countrySelectBox.appendChild(country_option)
                    })
                });
        }
        else if (selectedContinent === "Africa") {
            $.post("/api/countries/", {'continent': selectedContinent})
                .done(function(data) {
                    data.forEach(function(country) {
                        var country_option = document.createElement("option");
                        country_option.textContent = country.pk;
                        countrySelectBox.appendChild(country_option)
                    })
                });
        }
        else if (selectedContinent === "South America") {
            $.post("/api/countries/", {'continent': selectedContinent})
                .done(function(data) {
                    data.forEach(function(country) {
                        var country_option = document.createElement("option");
                        country_option.textContent = country.pk;
                        countrySelectBox.appendChild(country_option)
                    })
                });
        }
        else if (selectedContinent === "North America") {
            $.post("/api/countries/", {'continent': selectedContinent})
                .done(function(data) {
                    data.forEach(function(country) {
                        var country_option = document.createElement("option");
                        country_option.textContent = country.pk;
                        countrySelectBox.appendChild(country_option)
                    })
                });
        }
    }


};
