function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
document.addEventListener('DOMContentLoaded', function() {


    let modalButtons = document.querySelectorAll('.popUpBtn'),
        overlay      = document.querySelector('#overlay-modal'),
        closeButtons = document.querySelectorAll('.cross');

    modalButtons.forEach(function(item){

        item.addEventListener('click', function(e) {

            e.preventDefault();
            let butAttr = this.getAttribute('id');
            if (butAttr === 'log') {
                let modal = document.querySelector('#popUpLog');
                modal.style.display = 'block';
                overlay.style.display = 'block';
            } else if (butAttr === 'reg') {
                let modal = document.querySelector('#popUpReg');
                modal.style.display = 'block';
                overlay.style.display = 'block';
            } else if (butAttr === 'cart1') {
                let modal = document.querySelector('.basket');
                modal.style.display = 'block';
            } else if (butAttr === 'cart2') {
                let modal = document.querySelector('.basket');
                modal.style.display = 'block';
            }
      });
    });

    closeButtons.forEach(function (item) {
        item.addEventListener('click', function(e) {

            e.preventDefault()
            overlay.style.display = 'none';
            document.querySelectorAll('.popup').forEach(function (item) {
                item.style.display = 'none';
            })
            document.querySelectorAll('.basket').forEach(function (item) {
                item.style.display = 'none';
            })
        })
    });
}); // end ready

$('#productModal').on('show.bs.modal', function (event) {
    alert('123')
    let button = $(event.relatedTarget);
    let url = button.data('url');
    let container = $(this).find('.good_body');
    container.html('');
    $.ajax({
        url: url,
    }).done(function (data){
        container.html(data);
    })
})


    // const exampleEl2 = document.querySelector('#ajax-example-2');
    // exampleEl2.addEventListener('click', function() {
    //     let xhr = new XMLHttpRequest();
    //     xhr.open('POST', 'ajax/example2/', true);
    //     xhr.addEventListener("readystatechange", function () {
    //         if ( (xhr.readyState==4) && (xhr.status==200) ) {
    //             let data = JSON.parse(xhr.response);
    //             const response = document.querySelector('.ajax-example-2-response-2');
    //             response.innerHTML = data.message;
    //         }
    //     });
    //     const CSRFToken = getCookie('csrftoken')
    //     xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    //     xhr.setRequestHeader("X-CSRFToken", CSRFToken);
    //     xhr.send();
    // });
