function form_submit(){

    let csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    let form_data = $("form").serializeArray();
    let subject_id = $("#subject_id_input").val();

    $.ajax({
        url: "/testing/subjects/" + subject_id +"/tests/add",
        method: "POST",
        dataType: 'json',
        data: form_data,
        timeout : 100000,
        success: function (data) {
            // console.log(data);
            if (data['error']) {
                alert(data['error']);
            } else {
                window.opener.location.href = window.opener.location.href;
                window.close();
            }
        },
        error: function (e) {
            console.log("ERROR: ", e);
        },
        done: function (e) {
            console.log("DONE");
        }
    });
}

$("#testing_form").submit(function(event) {
    event.preventDefault();
    event.stopPropagation();

    var form = document.getElementsByClassName('needs-validation');

    if (form[0].checkValidity() === true) {
        form_submit();
    }
    form[0].classList.add('was-validated');

});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

