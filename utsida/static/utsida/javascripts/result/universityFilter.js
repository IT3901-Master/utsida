(function() {

    var s;

    UniversityFilter = {

        settings: {
            selected_university: null
        },

        init: function() {
            s = this.settings;
        },

        filter: function(box) {
            s.selected_university = box.children[0].innerHTML.replace(/ *\([^)]*\) */g, "");
            window.location = "/process/result/" + s.selected_university + '/';
        }

    };

    UniversityFilter.init();

})();

