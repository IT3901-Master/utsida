$(document).ready(function () {
    var institute = $("#institute")[0].innerHTML;
    var continent = $("#continent")[0].innerHTML;
    var country = $("#country")[0].innerHTML;
    var university = $("#university")[0].innerHTML;
    var language = $("#language")[0].innerHTML;
    var studyPeriod = $("#studyPeriod")[0].innerHTML;
    var academicQuality = $("#academicQuality")[0].innerHTML;
    var socialQuality = $("#socialQuality")[0].innerHTML;

    var queryContent = JSON.stringify({
        "Institute": institute,
        "Continent": continent,
        "Country": country,
        "University": university,
        "Language": language,
        "StudyPeriod": studyPeriod,
        "AcademicQuality": academicQuality,
        "SocialQuality": socialQuality
    });

    // Querying the myCBR server with the selected attributes
    $.ajax({
        type: "POST",
        url: "http://localhost:8080/retrieval?casebase=main_case_base&concept%20name=Trip",
        data: queryContent,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (res) {
            console.log(res.similarCases);
            var resultList = res.similarCases;
            var caseList = [];

            var caseContaier = document.getElementById("results");

            var counter = 0;

            // Querying each single case retrieved for the full information
            $.each(resultList, function(key, value) {
                $.ajax("http://localhost:8080/case?caseID=" + key).done(function(res) {
                    var case_university = res.case.University;
                    var case_subjects = res.case.Subjects.split('!');

                    // Creating all the HTML elements
                    var panelContainer = document.createElement("div");
                    var panel = document.createElement("div");
                    var panelHeading = document.createElement("div");
                    var panelBody = document.createElement("div");
                    var panelTitleUniveristy = document.createElement("span");
                    var panelTitleSimilarity = document.createElement("span");
                    var panelList = document.createElement("ul");
                    var hiddenInformation = document.createElement("ul");
                    var hiddenInstitute = document.createElement("li");
                    var hiddenContinent = document.createElement("li");
                    var hiddenCountry = document.createElement("li");
                    var hiddenUniversity = document.createElement("li");
                    var hiddenLanguage = document.createElement("li");
                    var hiddenStudyPeriod = document.createElement("li");
                    var hiddenAcademicQuality = document.createElement("li");
                    var hiddenSocialQuality = document.createElement("li");

                    // Adding css to the created HTML elements
                    panelContainer.className = "col-md-4";
                    panelContainer.id = counter;
                    panel.className = "panel panel-primary square-corners";
                    panelHeading.className = "panel-heading square-corners";
                    panelBody.className = "panel-body";
                    panelTitleSimilarity.className = "pull-right";
                    hiddenInformation.className = "hidden";

                    // Creates a list element for each subject selected
                    for (var i = 0; i < case_subjects.length; i++) {
                        var listElement = document.createElement("li");
                        listElement.innerHTML = case_subjects[i];
                        panelList.appendChild(listElement);
                    }

                    // Adding all data to the created HTML elements
                    panelTitleUniveristy.innerHTML = case_university;
                    panelTitleSimilarity.innerHTML = value;
                    hiddenInstitute.innerHTML = res.case.Institute;
                    hiddenContinent.innerHTML = res.case.Continent;
                    hiddenCountry.innerHTML = res.case.Country;
                    hiddenUniversity.innerHTML = res.case.University;
                    hiddenLanguage.innerHTML = res.case.Language;
                    hiddenStudyPeriod.innerHTML = res.case.StudyPeriod;
                    hiddenAcademicQuality.innerHTML = res.case.AcademicQuality;
                    hiddenSocialQuality.innerHTML = res.case.SocialQuality;

                    // Creates the HTML layout
                    hiddenInformation.appendChild(hiddenInstitute);
                    hiddenInformation.appendChild(hiddenContinent);
                    hiddenInformation.appendChild(hiddenCountry);
                    hiddenInformation.appendChild(hiddenUniversity);
                    hiddenInformation.appendChild(hiddenLanguage);
                    hiddenInformation.appendChild(hiddenStudyPeriod);
                    hiddenInformation.appendChild(hiddenAcademicQuality);
                    hiddenInformation.appendChild(hiddenSocialQuality);
                    panelHeading.appendChild(panelTitleUniveristy);
                    panelHeading.appendChild(panelTitleSimilarity);
                    panelBody.appendChild(panelList);
                    panelBody.appendChild(hiddenInformation);
                    panel.appendChild(panelHeading);
                    panel.appendChild(panelBody);
                    panelContainer.appendChild(panel);
                    caseContaier.appendChild(panelContainer);
                });
            });
        },
        failure: function (res) {
            console.log("ERROR" + res)
        }
    });
});