(function() {

    var s;

    UniversityFilter = {

        settings: {
            selector: $('#universitySelector'),
            selected_university: null
        },

        init: function() {
            s = this.settings;
            this.updateSelector();
        },

        filter: function() {
            s.selected_university = s.selector.find(":selected").val();
            window.location = "/process/result/" + s.selected_university + '/';
        },

        updateSelector: function() {
            var uni = decodeURI(window.location.href.split('/').slice(-2, -1)[0]);
            s.selector.val(uni).prop('selected', true);
        }

    };

    UniversityFilter.init();

})();