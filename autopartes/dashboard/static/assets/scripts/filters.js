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

$(document).ready(function () {
    var request;

    request = $.ajax({
        url: "/shop/get_models/",
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': "application/json;charset=UTF-8"
        },
        data:
            {
                brand: $("#brand_car_filter").val()
            }
    });

    request.done(function (msg) {
        $("#model_car_filter").empty()
        var models = JSON.parse(msg);
        $("#model_car_filter").append(new Option("Modelos", ""));
        $.each(models, function (i, val) {
            $("#model_car_filter").append(new Option(val, val));
        });

        var aux;

        aux = $.ajax({
            url: "/shop/get_years/",
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': "application/json;charset=UTF-8"
            },
            data:
                {
                    model: $("#model_car_filter").val()
                }
        });

        aux.done(function (msg) {
            $("#year_car_filter").empty()
            var years = JSON.parse(msg);
            $("#year_car_filter").append(new Option("Años", ""));
            $.each(years, function (i, val) {
                $("#year_car_filter").append(new Option(val, val));
            });
        });

    });


    var products = $.ajax({
        url: "/shop/get_product_names/",
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': "application/json;charset=UTF-8"
        }
    });

    products.done(function(msg){
        var prodText = []

        var products = JSON.parse(msg);
        $.each(products, function (i, val) {
            prodText.push(val)
        });

        $(function() {

            $("#text_filter").autocomplete({
                source: prodText,
                autoFocus:true
            });
        });


    });

});

$("#brand_car_filter").change(function () {
    var request;

    request = $.ajax({
        url: "/shop/get_models/",
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': "application/json;charset=UTF-8"
        },
        data:
            {
                brand: $("#brand_car_filter").val()
            }
    });

    request.done(function (msg) {
        $("#model_car_filter").empty()
        var models = JSON.parse(msg);
        $("#model_car_filter").append(new Option("Modelos", ""));
        $.each(models, function (i, val) {
            $("#model_car_filter").append(new Option(val, val));
        });

        var aux;

        aux = $.ajax({
            url: "/shop/get_years/",
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': "application/json;charset=UTF-8"
            },
            data:
                {
                    model: $("#model_car_filter").val()
                }
        });

        aux.done(function (msg) {
            $("#year_car_filter").empty()
            var years = JSON.parse(msg);
            $("#year_car_filter").append(new Option("Años", ""));
            $.each(years, function (i, val) {
                $("#year_car_filter").append(new Option(val, val));
            });
        });

    });
});

$("#model_car_filter").change(function () {
    var request;

    request = $.ajax({
        url: "/shop/get_years/",
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': "application/json;charset=UTF-8"
        },
        data:
            {
                model: $("#model_car_filter").val()
            }
    });

    request.done(function (msg) {
        $("#year_car_filter").empty();
        var years = JSON.parse(msg);
        $("#year_car_filter").append(new Option("Años", ""));
        $.each(years, function (i, val) {
            $("#year_car_filter").append(new Option(val, val));
        });
    });
});

