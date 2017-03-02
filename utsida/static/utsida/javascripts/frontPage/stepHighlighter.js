(function() {
    var s;

    stepHighlighter = {

        settings: {
            num1: $('#number1'),
            num2: $('#number2'),
            num3: $('#number3'),

            col1: $('#col1'),
            col2: $('#col2'),
            col3: $('#col3'),

            btn1: $('#front-btn-1'),
            btn2: $('#front-btn-2'),
            btn3: $('#front-btn-3'),
            btn4: $('#front-btn-4')
        },

        init: function () {
            s = this.settings;

            s.num1.mouseover(function() {
                s.col1.css('background-color', '#d9d9d9');
            });
            s.num1.mouseleave(function() {
                s.col1.css('background-color', 'white');
            });

            s.num2.mouseover(function() {
                s.col2.css('background-color', '#d9d9d9');
            });
            s.num2.mouseleave(function() {
                s.col2.css('background-color', 'white');
            });

            s.num3.mouseover(function() {
                s.col3.css('background-color', '#d9d9d9');
            });
            s.num3.mouseleave(function() {
                s.col3.css('background-color', 'white');
            });


            s.btn1.mouseover(function() {
                s.num1.popover('toggle');
                s.col1.css('background-color', '#d9d9d9');
            });
            s.btn1.mouseleave(function() {
                s.num1.popover('hide');
                s.col1.css('background-color', 'white');
            });

            s.btn2.mouseover(function() {
                s.num2.popover('toggle');
                s.col2.css('background-color', '#d9d9d9');
            });
            s.btn2.mouseleave(function() {
                s.num2.popover('hide');
                s.col2.css('background-color', 'white');
            });

            s.btn3.mouseover(function() {
                s.num2.popover('toggle');
                s.col2.css('background-color', '#d9d9d9');
            });
            s.btn3.mouseleave(function() {
                s.num2.popover('hide');
                s.col2.css('background-color', 'white');
            });

            s.btn4.mouseover(function() {
                s.num3.popover('toggle');
                s.col3.css('background-color', '#d9d9d9');
            });
            s.btn4.mouseleave(function() {
                s.num3.popover('hide');
                s.col3.css('background-color', 'white');
            })
        },
    };

    stepHighlighter.init();

})();

