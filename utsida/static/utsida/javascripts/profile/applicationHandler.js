//documentation: http://bootstrap-confirmation.js.org/
$('[data-toggle=confirmation]').confirmation({
            rootSelector: '[data-toggle=confirmation]',
			onConfirm: function() {
                var here = this;
                var block = $(this).context.parentNode.parentNode.parentNode;
                var id = $(this)[0].dataset["id"];
                var type = $(this)[0].dataset["type"];
                $.post("/profile/remove_application/", {'id': id});
                $(this).closest('.courseBlock').fadeOut("slow",function(here) {block.parentNode.removeChild(block)});

            },
            title: "Sikker på at du vil slette?",
            btnOkLabel: "Ja",
            btnCancelLabel: "Nei",
            singleton: true,
            popout: true,
            placement: "right",
            container: "body"

		});

