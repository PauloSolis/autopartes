if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}

function ready() {
    //sc = shopping cart
    localStorage.clear()
    var sc = JSON.parse(localStorage.getItem('local_shopping_cart'));
    if (sc != null) {
        for (i = 0; i < sc.length; i++) {
            var product = JSON.parse(sc[i])
            //alert(product)
            addItemToCart(product.prod_id, product.prod_title, product.prod_quantity, product.price_at_sale, product.prod_image)
        }

    }
    updateCartTotal()

    var removeCartItemButtons = document.getElementsByClassName('btn-danger')
    for (var i = 0; i < removeCartItemButtons.length; i++) {
        var button = removeCartItemButtons[i]
        button.addEventListener('click', removeCartItem)
    }

    var quantityInputs = document.getElementsByClassName('cart-quantity-input')
    for (var i = 0; i < quantityInputs.length; i++) {
        var input = quantityInputs[i]
        input.addEventListener('change', quantityChanged)
    }

    var addToCartButtons = document.getElementsByClassName('shop-item-button')
    for (var i = 0; i < addToCartButtons.length; i++) {
        var button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked)
    }

    document.getElementsByClassName('btn-purchase')[0].addEventListener('click', purchaseClicked)
}

function purchaseClicked() {
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var total = 0
    var cart = {products: [], data: []};
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var idElement = cartRow.getElementsByClassName('cart-item-id')[0]
        var priceElement = cartRow.getElementsByClassName('cart-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var id = parseInt(idElement.innerText)
        var price = parseFloat(priceElement.innerText.replace('$', ''))
        var quantity = quantityElement.value

        var obj = {prod_id: id, prod_quantity: quantity, price_at_sale: price}
        cart.products.push(JSON.stringify(obj))

        total = total + (price * quantity)
    }

    cart.data.push(JSON.stringify({total: [total]}));

    var addresses = document.getElementsByName('address');
    var selected_address = false;
    for (var i = 0; i < addresses.length; i++) {
        if (addresses[i].checked) {
            selected_address = addresses[i].value;
            break;
        }
    }
    if (!selected_address) {
        alert("elige una direccion de envio")

    } else {
        cart.data.push(JSON.stringify({address: [selected_address]}))
        alert(selected_address)
        json = JSON.stringify(cart);
        var xhr = new XMLHttpRequest();
        var url = "/orders/store_order/";
        var token = getCookie('csrftoken');

        var redirect = '';

        xhr.open("POST", url, true);
        xhr.setRequestHeader("X-CSRFToken", token);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var json = JSON.stringify(xhr.responseText);
                console.log(json);

            }
        };

        xhr.send(json);

        var cartItems = document.getElementsByClassName('cart-items')[0]
        while (cartItems.hasChildNodes()) {
            cartItems.removeChild(cartItems.firstChild)
        }
        updateCartTotal();
    }


}

function removeCartItem(event) {
    var buttonClicked = event.target
    removeFromResume(buttonClicked.value)
    buttonClicked.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.remove()
    updateCartTotal()
}
function removeFromResume(prod_id){
    document.getElementById("short_cart"+prod_id).remove()
}

function quantityChanged(event) {
    var input = event.target
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1
    }
    updateCartTotal()
}

function addToCartClicked(event) {

    var button = event.target
    var shopItem = button.parentElement.parentElement.parentElement.parentElement
    var prod_id = shopItem.getElementsByClassName('product-id')[0].innerText
    var title = shopItem.getElementsByClassName('shop-item-title')[0].innerText
    var description = shopItem.getElementsByClassName('product-description')[0].innerText
    var price = shopItem.getElementsByClassName('shop-item-price')[0].innerText
    var quantity = shopItem.getElementsByClassName('shop-item-quantity')[0].value
    var image = shopItem.getElementsByClassName('shop-image-product')[0].src
    addItemToCart(prod_id, title,description, quantity, price, image)
    updateCartTotal()
}

function addItemToCart(prod_id, title, description, quantity, price, imageSrc) {
    var cartRow = document.createElement('div')
    cartRow.classList.add('cart-row')
    var cartItems = document.getElementsByClassName('cart-items')[0]
    var cartItemNames = cartItems.getElementsByClassName('cart-item-title')
    var cartResume = document.getElementById('resumen')
    for (var i = 0; i < cartItemNames.length; i++) {
        if (cartItemNames[i].innerText == title) {
            alert('This item is already added to the cart')
            return
        }
    }
    var total_price = parseFloat(price.replace('$', '')) * quantity
    var cartRowContents = `
        <br>
        <div class="row">
            <div class="col-md-5">
                <img class="cart-product-image" style="height: 16vh;" src="${imageSrc}">
            </div>
            <div class="col-md-7">
                <div class="cart-item cart-column">
                    <span class="cart-item-title">${title}</span>
                <div class="cart-item-id cart-column" style="display:none">${prod_id}</div>
                <div class="cart-quantity cart-column">
                    <input class="cart-quantity-input" type="number" value="${quantity}">
                    <span class="base-price hidden">${price}</span>
                    <span class="cart-price cart-column" >$${total_price}</span>
                    <span><button class="btn btn-danger" value="${prod_id}" type="button" style="float:right;"><i class="fa fa-trash fa-fw"></i></button></span>
                </div>    
                
            </div>
        </div>  
        `


    cartResume.innerHTML += `
    <span id="short_cart${prod_id}">
        <div class="col-md-3" >
           <h6>${title}</h6>
        </div>
        <div class="col-md-3">
            <h6>${description}</h6>
        </div>
        <div class="col-md-3">
            <h6 type="number" value="${quantity}">${quantity}</h6>
        </div>
        <div class="col-md-3">
            <h6 class="cart-price cart-column" >$${total_price}</h6>
        </div>
    </span>
        `
    cartRow.innerHTML = cartRowContents
    cartItems.append(cartRow)
    cartRow.getElementsByClassName('btn-danger')[0].addEventListener('click', removeCartItem)
    cartRow.getElementsByClassName('cart-quantity-input')[0].addEventListener('change', quantityChanged)
}

function updateCartTotal() {
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var total = 0
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('base-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var price = parseFloat(priceElement.innerText.replace('$', ''))
        var quantity = quantityElement.value
        cartRow.getElementsByClassName("cart-price")[0].innerHTML = "$" + price * quantity
        total = total + (price * quantity)
    }
    total = Math.round(total * 100) / 100
    document.getElementsByClassName('header-cart-count')[0].innerHTML = cartRows.length
    document.getElementsByClassName('cart-total-price')[0].innerText = '$' + total

    document.getElementsByClassName('cart-total-price-outside')[0].innerText = '$' + total
    document.getElementsByClassName('cart-total-price-to-pay')[0].innerText = '$' + total

    var local = []
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var idElement = cartRow.getElementsByClassName('cart-item-id')[0].innerText
        var titleElement = cartRow.getElementsByClassName('cart-item-title')[0].innerText
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0].value
        var priceElement = cartRow.getElementsByClassName('cart-price')[0].innerText
        var imageElement = cartRow.getElementsByClassName('cart-product-image')[0].src

        var obj = {
            prod_id: idElement,
            prod_title: titleElement,
            prod_quantity: quantityElement,
            price_at_sale: priceElement,
            prod_image: imageElement
        }
        local.push(JSON.stringify(obj))
    }
    localStorage.setItem('local_shopping_cart', JSON.stringify(local));
}

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