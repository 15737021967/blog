$("[name='code-btn']").click(function () {
    $.ajax({
        url: '/forget-password/',
        type: 'post',
        dataType: 'JSON',
        data: {
            'status': 1,
            'account': $("[name='account']").val(),
            'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
        },
        success: function (rep) {
            alert(rep)
        }
    })
})
$("[name='submit-btn']").click(function () {
    $.ajax({
        url: '/forget-password/',
        type: 'post',
        dataType: 'JSON',
        data: {
            'status': 2,
            'account': $("[name='account']").val(),
            'code': $("[name='code']").val(),
            'password': $("[name='password']").val(),
            'confirm_password': $("[name='confirm_password']").val(),
            'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
        },
        success: function (rep) {
            alert(rep)
        }
    })
})