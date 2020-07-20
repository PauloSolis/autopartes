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
            $.each(years, function (i, val) {
                $("#year_car_filter").append(new Option(val, val));
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
        $("#year_car_filter").empty()
        var years = JSON.parse(msg);
        $.each(years, function (i, val) {
            $("#year_car_filter").append(new Option(val, val));
        });
    });
});


/*
<section class="b-goods-1 b-goods-1_mod-a">
                <div class="row">
                    <div>
                        <div class="b-goods-1__img col-md-8">
                            <a class="js-zoom-images "
                               href="{{ product.image2.url }}">
                                <img class="img-responsive center-block shop-image-product"
                                     src="{{ product.image1.url }}" alt="foto"/>
                            </a>
                            <span class="b-goods-1_price hidden-th">{{ product.public_price }}</span>
                        </div>
                        <div class="b-goods-1__inner row">
                            <div class="b-goods-1_header col-md-8"><a class="b-goods-1_choose hidden-th"
                                                                      href="listing-1.html"><i
                                    class="icon fa fa-heart-o"></i></a>
                                <h2 class="shop-item-title b-goods-1__name">{{ product.name }} {{ product.description }}</h2>
                                <div hidden class="product-description"> {{ product.name }} {{ product.description }}
                                </div>
                                <br>

                            </div>
                            <div class="hidden product-id" value="{{ product.id }}">{{ product.id }}</div>
                            <div class="b-goods-1__info col-md-12 product-code"> {{ product.product_code }}
                            </div>
                            {% if user.is_retailer %}
                                <span class="shop-item-price b-goods-1_price_th text-primary visible-th col-md-12"
                                      value="{{ product.public_price }}">$ {{ product.public_price }}
                                            </span>
                            {% endif %}
                            {% if user.is_wholesaler %}
                                <span class="shop-item-price b-goods-1_price_th text-primary visible-th col-md-12">$ {{ product.wholesale_price }}
                                            </span>
                            {% endif %}
                            <div class="b-goods-1__section">
                                <div class="collapse in" id="desc-1">
                                    <ul class="b-goods-1__desc list-unstyled">
                                        <li class="b-goods-1__desc-item">{{ product.car_brand }}</li>
                                        <li class="b-goods-1__desc-item">{{ product.car_model }}</li>
                                        <li class="b-goods-1__desc-item">{{ product.car_year }}</li>
                                    </ul>
                                </div>
                            </div>
                            <br>
                            <div class="row">
                                <div class="col-md-6">
                                    <input class="cart-quantity-input shop-item-quantity" type="number" value="1"
                                           min="1"
                                           max="1000" step="1"/>
                                    <br><br>
                                    {% if product.in_stock > 20 %}
                                        <p style="color: #d01818; font-size: medium;">En stock</p>
                                    {% endif %}
                                    {% if product.in_stock > 0 and product.in_stock < 20 %}
                                        <p style="color: #d01818; font-size: medium;">{{ product.in_stock }} en
                                            stock</p>
                                    {% endif %}
                                    {% if product.in_stock == 0 %}
                                        <p style="color: #d01818; font-size: medium;">No disponible</p>
                                    {% endif %}
                                </div>
                                {% if product.in_stock != 0 %}
                                    <div class="col-md-6">
                                        <button class="btn btn-primary shop-item-button" type="button">ADD TO CART
                                        </button>
                                    </div>
                                {% endif %}
                            </div>

                        </div>
                    </div>
                </div>
            </section>
 */