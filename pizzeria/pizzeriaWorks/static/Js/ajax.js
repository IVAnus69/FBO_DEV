$(document).ready(function () {
    const d1 = $.Deferred();
    const d2 = $.Deferred();

    $('.attention').fadeIn(3000, d1.resolve);

    d1.done(function () {
        $('.attention').fadeOut(3000, d2.resolve);
    });

    $.ajax({
        url: 'ajax/resp',
        method: 'GET',
        dataType: 'json',
        success: function (data){
            alert(data['text'])
        }
    })
})





$("#id_email").onchange(function () {
    alert("1312")
    let url = "/jqajax/checkemail/";
    let email = $(this).val();
    $.ajax({
        url: url,
        data: {
        csrfmiddlewaretoken: getCookie(),
        email: email
        },
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            $("span.ajax-response").html(data.message);
        },
     error: function (e) {
        console.log(e);
     },
     });
 });

