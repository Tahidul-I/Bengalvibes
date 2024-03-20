$(document).ready(function() {

    $(".choose-size").hide();

    // show sizes based on color
    $(document).on('click', '.choose-color', function() {
        console.log("sdfgeyrfgeryfg8erferf");
        $(".choose-color").removeClass('active-item');
        $(this).addClass('active-item');

        var _color = $(this).data('color');
        $('#product_color').attr('value',_color);
        // Hide all sizes and remove 'active-item' class
        $(".choose-size").hide().removeClass('active-item');

        // Show sizes for the selected color
        $(".color" + _color).show();
        $(".color" + _color).first().addClass('active-item');
        var _size =  $(".color" + _color).first().attr('data-size-id');
        $('#product_size').attr('value',_size);
        

        var _price = $(".color" + _color).first().attr('data-price');
        $(".products-price").text(_price);
        $('#product_price').attr('value',_price);
        

    });

    // Show Price according to selected size
    $(document).on('click', '.choose-size', function() {
        $(".choose-size").removeClass('active-item');
        $(this).addClass('active-item');
        var _size = $(this).attr('data-size-id');
        $('#product_size').attr('value',_size);
        var _price = $(this).attr('data-price');
        $('#product_price').attr('value',_price);
        $(".products-price").text(_price);
        

    });

    // Show the first selected color on page load
    $(".choose-color").first().addClass('active-item');
    var _color = $(".choose-color").first().data('color');
    $('#product_color').attr('value',_color);
    $(".color" + _color).show();
    var _size = $(".color" + _color).attr('data-size-id');
    $('#product_size').attr('value',_size);
    $(".color" + _color).first().addClass('active-item');
    var _price = $(".color" + _color).first().attr('data-price');
    $('#product_price').attr('value',_price);
    $(".products-price").text(_price);
    


    $('#addToCartBtn').click(function (e) {
        e.preventDefault();

        var product_id = $('#product-id').val();
        var product_title = $('#product-title').val();
        var product_quantity = $('#product-quantity').val();
        var token =  $('input[name=csrfmiddlewaretoken]').val();
        var color_id = $(".choose-color.active-item").data('color');
        var selectedSizeElement = $(".choose-size.active-item");
        var size_id = selectedSizeElement.data('size-id');
        console.log(color_id);
        $.ajax({
            type: "POST",
            url: "/add-to-cart",
            data: {
                'product_id':product_id,
                'product_title':product_title,
                'product_quantity':product_quantity,
                'color_id': color_id,
                'size_id': size_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                if(response.total_cart_quantity){
                    $('#total_cart_quantity').text(response.total_cart_quantity)
                }
                if (response.success_status){
                    alertify.success(response.success_status)
                }
                if(response.error_status){
                    alertify.error(response.error_status)
                }
                if(response.warning_status){
                    alertify.warning(response.warning_status)
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("AJAX Request Failed: " + textStatus, errorThrown);
            }

        });
    });

    $('#addToCartBtn_anonymous').click(function (e) {
        e.preventDefault();
        var csrf_token = document.cookie.match(/csrftoken=([^ ;]+)/)[1];
        var product_id = $('#product-id').val();
        var color_id = $('#product_color').val();
        var size_id = $('#product_size').val();
        var product_price = $('#product_price').val();
        var product_quantity = $('#product-quantity').val();
        var product_image = $('.product_related_image').first().attr('src');

        $.ajax({
            url:'/add-to-cart-anonymous/',
            type: 'POST', 
            contentType: 'application/json',
            data:JSON.stringify({
                'product_id':product_id,
                'color_id': color_id,
                'size_id': size_id,
                'product_price': product_price,
                'product_quantity':product_quantity,
                'product_image':product_image
            }),
            headers: {
                'X-CSRFToken': csrf_token
            }, 
            success: function (response) {

                if(response.total_cart_items){
                    $('#total_cart_quantity').text(response.total_cart_items);
                }
                if(response.success_status){
                    alertify.success(response.success_status)
                }
                if(response.error_status){
                    alertify.error(response.error_status);
                }
                
               
            }
           

        });
    });


    $(document).on('click', '.increase_changeQuantity', function (e) {
        e.preventDefault();
        console.log("clicked");
        var product_id = $(this).closest('.product_data').find('.product-id').val();
        var product_quantity = parseInt($(this).closest('.product_data').find('#product_quantity').val())+1;
        var token =  $('input[name=csrfmiddlewaretoken]').val();
        console.log(product_id);
        console.log(product_quantity);
        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id':product_id,
                'product_quantity':product_quantity,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                $('#main_cart_table').html(response.update_cart_template);
                if (response.warning_status){
                    alertify.warning(response.warning_status)
                }
                else{
                    alertify.success(response.status)
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("AJAX Request Failed: " + textStatus, errorThrown);
            }

        });
    });

    $(document).on('click', '.reduce_changeQuantity', function (e) {
        e.preventDefault();
        var product_id = 0;
        var product_quantity = 0;
        var token =  $('input[name=csrfmiddlewaretoken]').val();
        var status = $(this).attr('data-status');
        if(status == "stock"){
            product_id = $('#stock_out_quantity').attr('data-id');
            product_quantity =parseInt( $('#stock_out_quantity').val()-1);
        }
        else{
            product_id = $(this).closest('.product_data').find('.product-id').val();
            product_quantity = parseInt($(this).closest('.product_data').find('#product_quantity').val())-1;

        }
        
        if(product_quantity==0){
            pass;
        }
        else{
            $.ajax({
                method: "POST",
                url: "/update-cart",
                data: {
                    'product_id':product_id,
                    'product_quantity':product_quantity,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    $('#main_cart_table').html(response.update_cart_template);
                    if (response.warning_status){
                        alertify.warning(response.warning_status)
                    }
                    else{
                        alertify.success(response.status)
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log("AJAX Request Failed: " + textStatus, errorThrown);
                }
    
            });

        }
        
        
    });
  
    $(document).on('click','.increase_changeQuantity_anonymous',function (e) {
        e.preventDefault();
        var product_variant_id = $(this).closest('.product_data').find('.product-id').val();
        var product_quantity = parseInt($(this).closest('.product_data').find('#product_quantity').val())+1;
        var token =  $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_variant_id':product_variant_id,
                'product_quantity':product_quantity,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                $('#main_cart_table').html(response.update_cart_template);
                if (response.warning_status){
                    alertify.warning(response.warning_status)
                }
                else{
                    alertify.success(response.status)
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("AJAX Request Failed: " + textStatus, errorThrown);
            }

        });
    });
    $(document).on('click','.reduce_changeQuantity_anonymous',function (e) {
        e.preventDefault();
        var product_variant_id = 0;
        var product_quantity = 0;
        var status = $(this).attr('data-status');
        var token =  $('input[name=csrfmiddlewaretoken]').val();
        if(status == "stock"){
            product_variant_id = $('#stock_out_quantity').attr('data-id');
            product_quantity =parseInt( $('#stock_out_quantity').val()-1);
        }
        else{
            product_variant_id = $(this).closest('.product_data').find('.product-id').val();
            product_quantity = parseInt($(this).closest('.product_data').find('#product_quantity').val())-1;

        }

        if(product_quantity==0){
            pass
        }
        else{
            $.ajax({
                method: "POST",
                url: "/update-cart",
                data: {
                    'product_variant_id':product_variant_id,
                    'product_quantity':product_quantity,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    $('#main_cart_table').html(response.update_cart_template);
                    if (response.warning_status){
                        alertify.warning(response.warning_status)
                    }
                    else{
                        alertify.success(response.status)
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log("AJAX Request Failed: " + textStatus, errorThrown);
                }
    
            });

        }

        
    });


    $('.cart_body').on('click', '.delete-cart-item', function (e) {
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.product-id').val()
        var token = $('input[name=csrfmiddlewaretoken]').val();
        console.log(product_id);
        var section_count = $('.product_data').length;
        console.log(section_count);
        $(this).closest('.product_data').hide();
    
        $.ajax({
            method: "POST",
            url: "delete-cart-item",
            data: {
                'product_id': product_id,
                'section_count':section_count,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                $('#total_cart_quantity').text(response.total_cart_quantity);
                if (response.message) {
                    $('.product_data').hide();
                    $('#cart_table_heading').hide();
                    $('#action_buttons').hide();
                    $('#empty_cart_row').show();
                    $('#empty_cart_row').html(response.message);
                } else {
                    alertify.success(response.status)
                    $('.cart_body').load(location.href + " .cart_body")
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("AJAX Request Failed: " + textStatus, errorThrown);
            }
        });
    });

    function validateNumericInput(input) {
        // Remove any non-numeric characters
         input.value = input.value.replace(/[^0-9]/g, '');
    }


    $(document).on('click','.payment_selection',function(){
        
        var mode = $(this).children('input').attr('value');
        console.log(mode);
        if(mode=="COD"){
            $('#payment_method').attr('value',mode);
        }
        else{
            $('#payment_method').attr('value',mode);
        }
       
    });


    $(document).on('click','#place_order_button',function(event){
        event.preventDefault();
        var payment_mode = $('#payment_method').attr('value');
        if (payment_mode=="PO"){
            alertify.confirm('Are you sure? ', 'Pressing Ok will take you to the online payment procedure', function(){ 
                document.getElementById('checkout_detail_form').submit();
             }
        , function(){ });
        }
        else{
            alertify.confirm('Are you sure? ', 'Pressing Ok will place your order which can not be cancelled', function(){ 
                document.getElementById('checkout_detail_form').submit();
             }
            , function(){ });
        }
        
    });


    $(document).on('click','#stock_out_btn',function(){
        alertify.error("Out Of Stock");
    })


    $(document).on('click','#cart_quantity_increase',function(){
        console.log("CLICKED");
        var quantity =parseInt( $('#product-quantity').val());
        console.log(quantity);
        quantity += 1;
        $('#product-quantity').val(quantity).trigger('input');
        console.log(quantity);
    })

    $(document).on('click','#cart_quantity_reduce',function(){
        var quantity =parseInt( $('#product-quantity').val());
        if(quantity == 1){
            pass
        }
        else{
            quantity -= 1;
        }
       
        $('#product-quantity').val(quantity).trigger('input');
    })






});
