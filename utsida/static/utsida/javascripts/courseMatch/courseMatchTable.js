/* Formatting function for row details - modify as you need */
function format(d) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td>Godkjent:  </td>' +
        '<td>' + d[4] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Universitet: </td>' +
        '<td>' + d[5] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Kommentar: </td>' +
        '<td>' + d[6] + '</td>' +
        '</tr>' +
        '</table>';
}


$(document).ready(function () {
    var table = $('#example').DataTable({
        initComplete: function () {
            this.api().columns('.select-filter').every(function () {
                var column = this;
                var select = $('<select class="form-control"><option value="" disabled selected>Velg Universitet</option><option value=""></option></select>')
                    .appendTo($('#selection').empty())
                    .on('change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );

                        column
                            .search(val ? '^' + val + '$' : '', true, false)
                            .draw();
                    });

                column.data().unique().sort().each(function (d, j) {
                    select.append('<option value="' + d + '">' + d + '</option>')
                });
            });
        },
        "order": [[1, 'asc']],
        "columnDefs": [
            {
                "targets": [0],
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            {
                "targets": [5],
                "visible": false
            },
            {
                "targets": [4],
                "visible": false
            },
            {
                "targets": [6],
                "visible": false
            }
        ]
    });

    $('#example tbody').on('click', 'td', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
            tr.children()[0].className = "glyphicon glyphicon-chevron-down"
        }
        else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
            tr.children()[0].className = "glyphicon glyphicon-chevron-up"
        }
    });
});