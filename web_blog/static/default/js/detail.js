$('.reply').click(function () {
        var id = $(this).attr('name')
        var reply_to = $(this).attr('reply_to')
        $('#id_parent').attr('value', id)
        $('#id_reply_to').attr('value', reply_to)
        $('#cancel').removeClass('hidden')
        $('#id_content').attr('placeholder', '想对 '+ reply_to + ' 说什么')
    })
$('#cancel').click(function () {
    var reply_to = $('.follow-name').text()
    $('#id_parent').attr('value', '')
    $('#id_reply_to').attr('value', reply_to)
    $('#id_content').attr('placeholder', '想对作者说什么')
    $(this).addClass('hidden')
})
$('#snap-btn').click(function () {
    $.ajax({
        url: '/comment/snap/',
        type: 'post',
        dataType: 'JSON',
        data: {
            'post_id': $(this).attr('name'),
            'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val()
        },
        success: function(rep){

            if (rep == true){
                $('#snap-btn').addClass('snap-btn')
            }else if(rep == "redirect"){
                window.location.href = "/login/"
            }
            else{
                $('#snap-btn').removeClass('snap-btn')
            }
        }

    })
})
$('#submit').click(function () {
    $.ajax({
        url: '/comment/comment/',
        type: 'post',
        dataType: 'JSON',
        data: $('#fm').serialize(),
        success: function (rep) {
            if (rep['succeed'] == true){
                alert('评论成功')
                window.location.reload(true)
            }else{
                alert(rep['errors'])
            }
        }
    })
})