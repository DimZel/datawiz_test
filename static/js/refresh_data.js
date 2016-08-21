/**
 * Created by dimze on 18.08.2016.
 */
function refresh_data() {
    var date_from = $('#date_from').val();
    var date_to = $('#date_to').val();
    if (date_from && date_to) {
        $('#refreshing_msg').show()
        $.get('/refresh/', {date_from: date_from, date_to: date_to}, function (data) {
            $('#data').html(data);
        });
    }
}

$(document).ajaxComplete(function( event,request, settings ) {
    $('#refreshing_msg').hide()
});