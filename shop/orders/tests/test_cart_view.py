def test_cart(api_client, product_factory, reverse_url,
              anydict, django_assert_num_queries):
    product_first = product_factory()
    product_last = product_factory()
    api_client.post('/api/cart/products/', {
        'product': reverse_url(
            'product-detail', kwargs={'pk': product_first.pk}),
        'quantity': 5
    })
    api_client.post('/api/cart/products/', {
        'product': reverse_url(
            'product-detail', kwargs={'pk': product_last.pk}),
        'quantity': 3
    })

    # Checking db queryies num, there should be 4 (not 6, as with N+1)
    with django_assert_num_queries(4):
        response = api_client.get('/api/cart/')

    assert response.data == anydict({'cart_products': [
        anydict({
            'product': anydict({'name': product_first.name}),
            'quantity': 5
        }),
        anydict({
            'product': anydict({'name': product_last.name}),
            'quantity': 3
        }),
    ]})

    response = api_client.delete('/api/cart/')
    assert response.status_code == 204
    response = api_client.get('/api/cart/')
    assert response.data == anydict({'cart_products': []})


def test_cart_delete(api_client):
    response = api_client.delete('/api/cart/')
    assert response.status_code == 204


def test_cart_update_is_not_allowed(api_client):
    response = api_client.put('/api/cart/', {})
    assert response.status_code == 405
    response = api_client.patch('/api/cart/', {})
    assert response.status_code == 405
