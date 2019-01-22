
function add_card(token, id) {

    item1 = id

    $.get( "/cart/", { item: item1 , csrfmiddlewaretoken: token }, function( data, status ) {
        alert(data)

    });
}

function updateCart(item, qty, del){
		var url = "/cart/" + '?' + 'item=' + item + '&qty=' + qty;
		if(del === true){
			url += '&delete=y';
		}
		return $.ajax({
			url: url,
			type: 'GET',
		}).promise();
	}

	$('.update-cart').on('input', function(){
		var qty = $(this).val();
		if(!qty){
		return ;
		}
		var item = $(this).data('item-id');
		var self = $(this);
		updateCart(item, qty).then(function(response){
			console.log(response);
			$('#cart-count-badge').text(response.cart_count);
			self.parent().next().text('Rs '+ response.item_total);
			$('#cart-price').text('Rs ' + response.cart_price);
		});
	});

	$('.remove-item').click(function(event){
		console.log($(this));
		var item = $(this).data('item-id');
		updateCart(item, 1, true).then(function(response){
			window.location.reload();
		});
	});