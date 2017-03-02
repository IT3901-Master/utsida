(function() {
    var s;

    stepHighlighter = {

        settings: {
            num1: document.getElementById("number1"),
            num2: document.getElementById("number2"),
            num3: document.getElementById("number3"),

            col1: document.getElementById("col1"),
            col2: document.getElementById("col2"),
            col3: document.getElementById("col3")
        },

        init: function () {
            s = this.settings;

            s.num1.addEventListener('mouseover', function () {
                s.col1.style.backgroundColor = "#d9d9d9";
            });
            s.num1.addEventListener('mouseout', function () {
                s.col1.style.backgroundColor = "white";
            });

            s.num2.addEventListener('mouseover', function () {
                s.col2.style.backgroundColor = "#d9d9d9";
            });
            s.num2.addEventListener('mouseout', function () {
                s.col2.style.backgroundColor = "white";
            });

            s.num3.addEventListener('mouseover', function () {
                s.col3.style.backgroundColor = "#d9d9d9";
            });
            s.num3.addEventListener('mouseout', function () {
                s.col3.style.backgroundColor = "white";
            });
        },

    };

    stepHighlighter.init();

})();
