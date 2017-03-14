/* Formatting function for row details - modify as you need */
function format(d) {
    // `d` is the original data object for the row
    return '<table class="course-match-details" cellpadding="5" cellspacing="2" border="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td class="bold">Godkjent:  </td>' +
        '<td>' + d[4] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td class="bold">Universitet: </td>' +
        '<td>' + d[5] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td class="bold">Kommentar: </td>' +
        '<td>' + d[6] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td class="bold">Studiepoeng: </td>' +
        '<td>' + d[3] + '</td>' +
        '</tr>' +
        '</table>' +
        '<button class="btn btn-primary" onclick="addCourseMatch('+d[8]+')" style="margin-top: 5px;">' + 'Legg til i dine fag'+  '</button>';
}


$(document).ready(function () {


    var table = $('#example').DataTable({
        "order": [[1, 'asc']],
        "columnDefs": [
            {
                "targets": [0],
                "orderable": false,
                "defaultContent": ''
            },
            {
                "targets": [3],
                "visible": false
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
                "visible": false,
            },
            {
                "targets": [7],
                "orderable": false,
                "defaultContent": '',
                "width": "4.5%"
            },
            {
                "targets": [8],
                "visible": false
            }
        ]
    });

    //Shows the table after loading
    $('#example').css('opacity', 1);

    $('#example tbody').on('click', 'td', function () {
        var tr = $(this).closest('tr');
        var td = $(this).closest('td')[0].className;
        var row = table.row(tr);
        if (td == "editRow") {
            return;
        }
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
