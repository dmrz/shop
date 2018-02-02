def test_cart_product_create(
        api_client, anydict, product_factory, reverse_url):
    product = product_factory()
    response = api_client.post('/api/cart/products/', {
        'product': reverse_url('product-detail', kwargs={'pk': product.pk}),
        'quantity': 5
    })
    assert response.status_code == 201
    response = api_client.post('/api/cart/products/', {
        'product': reverse_url('product-detail', kwargs={'pk': product.pk}),
        'quantity': 5
    })
    assert response.status_code == 409
    assert response.data == {
        'cart': ['Duplicate entry'],
        'product': ['Duplicate entry']
    }


def test_cart_product_create_malformed(api_client):
    response = api_client.post('/api/cart/products/', {'x': 1, 'y': 2})
    assert response.status_code == 400
    assert response.data == {
        'product': ['This field is required.'],
        'quantity': ['This field is required.']
    }


def test_cart_product_delete(api_client, product_factory, reverse_url):
    product = product_factory()
    response = api_client.post('/api/cart/products/', {
        'product': reverse_url('product-detail', kwargs={'pk': product.pk}),
        'quantity': 5
    })
    response = api_client.delete(response.data['url'])
    assert response.status_code == 204


def test_cart_product_update(
        api_client, anydict, product_factory, reverse_url):
    product = product_factory()
    response = api_client.post('/api/cart/products/', {
        'product': reverse_url('product-detail', kwargs={'pk': product.pk}),
        'quantity': 5
    })
    response = api_client.patch(response.data['url'], {'quantity': 3})
    assert response.status_code == 200
    response = api_client.get(response.data['url'])
    assert response.data == anydict({'quantity': 3})

    other_product = product_factory()
    response = api_client.patch(
        response.data['url'],
        {'product': reverse_url(
            'product-detail', kwargs={'pk': other_product.pk})})
    assert response.status_code == 200
    response = api_client.get(response.data['url'])
    assert response.data == anydict({
        'product': reverse_url(
            'product-detail', kwargs={'pk': other_product.pk})})


def test_cart_product_update_zero_or_negative_quantity(
        api_client, anydict, product_factory, reverse_url):
    product = product_factory()
    response = api_client.post('/api/cart/products/', {
        'product': reverse_url('product-detail', kwargs={'pk': product.pk}),
        'quantity': 5
    })
    cart_product_url = response.data['url']
    response = api_client.patch(cart_product_url, {'quantity': 0})
    assert response.status_code == 400
    assert response.data == {
        'quantity': ['Ensure this value is greater than or equal to 1.']
    }
    response = api_client.patch(cart_product_url, {'quantity': -1})
    assert response.status_code == 400
    assert response.data == {
        'quantity': ['Ensure this value is greater than or equal to 1.']
    }


def test_cart_product_update_malformed(
        api_client, product_factory, reverse_url):
    product = product_factory()
    response = api_client.post('/api/cart/products/', {
        'product': reverse_url('product-detail', kwargs={'pk': product.pk}),
        'quantity': 5
    })
    response = api_client.patch(response.data['url'], {'quantity': 'test'})
    assert response.status_code == 400
    assert response.data == {
        'quantity': ['A valid integer is required.']
    }


def test_cart_max_product(
        api_client, product_factory, reverse_url, settings):
    products = [product_factory() for x
                in range(settings.ORDERS_CART_MAX_PRODUCTS)]
    for product in products:
        response = api_client.post('/api/cart/products/', {
            'product': reverse_url(
                'product-detail', kwargs={'pk': product.pk}),
            'quantity': 1
        })
        assert response.status_code == 201

    product = product_factory()
    response = api_client.post('/api/cart/products/', {
        'product': reverse_url('product-detail', kwargs={'pk': product.pk}),
        'quantity': 1
    })
    assert response.status_code == 400
    assert response.data == {
        'cart': [f'Maximum number of cart products exceeded '
                 f'({settings.ORDERS_CART_MAX_PRODUCTS}).']
    }


def test_cart_product_max_quantity_update(
        api_client, product_factory, reverse_url, settings):
    product = product_factory()
    response = api_client.post('/api/cart/products/', {
        'product': reverse_url('product-detail', kwargs={'pk': product.pk}),
        'quantity': settings.ORDERS_CART_MAX_PRODUCTS_QUANTITY
    })
    assert response.status_code == 201
    response = api_client.patch(
        response.data['url'],
        {'quantity': settings.ORDERS_CART_MAX_PRODUCTS_QUANTITY + 1})
    assert response.status_code == 400
    assert response.data == {
        'quantity': [
            f'Ensure this value is less than or equal to '
            f'{settings.ORDERS_CART_MAX_PRODUCTS_QUANTITY}.']
    }


def test_cart_product_max_quantity_create(
        api_client, product_factory, reverse_url, settings):
    product = product_factory()
    response = api_client.post('/api/cart/products/', {
        'product': reverse_url('product-detail', kwargs={'pk': product.pk}),
        'quantity': settings.ORDERS_CART_MAX_PRODUCTS_QUANTITY + 1
    })
    assert response.status_code == 400
    assert response.data == {
        'quantity': [
            f'Ensure this value is less than or equal to '
            f'{settings.ORDERS_CART_MAX_PRODUCTS_QUANTITY}.']
    }
