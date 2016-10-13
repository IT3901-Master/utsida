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

            $.each(resultList, function(key, value) {
                $.ajax("http://localhost:8080/case?caseID=" + key).done(function(res) {
                    var case_university = res.case.University;
                    var case_subjects = res.case.Subjects.split('!');

                    var panelContainer = document.createElement("div");
                    var panel = document.createElement("div");
                    var panelHeading = document.createElement("div");
                    var panelBody = document.createElement("div");
                    var panelTitleUniveristy = document.createElement("span");
                    var panelTitleSimilarity = document.createElement("span");
                    var panelList = document.createElement("ul");

                    panelContainer.className = "col-md-4";
                    panel.className = "panel panel-primary square-corners";
                    panelHeading.className = "panel-heading square-corners";
                    panelBody.className = "panel-body";
                    panelTitleSimilarity.className = "pull-right";

                    for (var i = 0; i < case_subjects.length; i++) {
                        var listElement = document.createElement("li");
                        listElement.innerHTML = case_subjects[i];
                        panelList.appendChild(listElement);
                    }

                    panelTitleUniveristy.innerHTML = case_university;
                    panelTitleSimilarity.innerHTML = value;
                    panelHeading.appendChild(panelTitleUniveristy);
                    panelHeading.appendChild(panelTitleSimilarity);
                    panelBody.appendChild(panelList);
                    panel.appendChild(panelHeading);
                    panel.appendChild(panelBody);
                    panelContainer.appendChild(panel);
                    caseContaier.appendChild(panelContainer)
                });
            });
        },
        failure: function (res) {
            console.log("ERROR" + res)
        }
    });
});