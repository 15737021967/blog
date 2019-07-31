$('#edit-button').on('click', function () {
    $('#edit-form').removeClass('hidden')
});
$('.close, .cancel').click(function () {
    $('#edit-form').addClass('hidden')
});
$('.confirm').click(function () {
    $.ajax({
        url: '/edit_info/',
        type: 'post',
        dataType: 'JSON',
        data: $('#fm').serialize(),
        success: function(rep){
            if (rep.status == true){
                window.location.reload(true)
            }else {
                alert(rep.msg)
            }
        }
    })
});
window.onload = function(){
    var date = $('#id_birthday').attr('value').replace(/\//g, '-')
    $('#id_birthday').attr('value', date)
}


