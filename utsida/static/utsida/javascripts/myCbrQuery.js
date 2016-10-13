 $(document).ready(function() {
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

            console.log('\n' + "-----------------------------------------------------------" + '\n' +
                        "Querying the myCBR project with the following attributes: " + '\n' +
                        "-----------------------------------------------------------" + '\n' +
                        "Institute: " + institute + '\n' +
                        "Continent: " + continent + '\n' +
                        "Country: " + country + '\n' +
                        "University: " + university + '\n' +
                        "Language: " + language + '\n' +
                        "StudyPeriod: " + studyPeriod + '\n' +
                        "AcademicQuality: " + academicQuality + '\n' +
                        "SocialQuality: " + socialQuality + '\n' +
                        "===========================================================" + '\n' +
                        "RESULTS" + '\n' +
                        "===========================================================");

            $.ajax({
                type: "POST",
                url: "http://localhost:8080/retrieval?casebase=main_case_base&concept%20name=Trip",
                data: queryContent,
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(res) {
                    console.log(res.similarCases);
                    $.ajax("http://localhost:8080/case?caseID=Trip0")
                            .done(function(singleCase) {
                                console.log(singleCase);
                    })
                },
                failure: function(res) {console.log("ERROR" + res)}
            });
        });