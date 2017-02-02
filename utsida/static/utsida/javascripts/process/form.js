/*
Logic for adding new form fields when they are appropriate to appear in /process.
 */

var formStep = function() {
    var selectedContinent = $("#continentField :selected").text();
    var countryRow = document.getElementById("countryRow");

    if (selectedContinent != "---------") {
        if (selectedContinent === "Asia") {

        }
        else if (selectedContinent === "Europa") {

        }
        else if (selectedContinent === "Oseania") {

        }
        else if (selectedContinent === "Afrika") {

        }
        else if (selectedContinent === "Sør-Amerika") {

        }
        else if (selectedContinent === "Nord-Amerika") {

        }
    }
};
