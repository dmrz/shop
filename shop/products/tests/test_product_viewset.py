def test_product_list(api_client, product_factory, reverse_url, anydict):
    product_first = product_factory()
    product_last = product_factory()
    response = api_client.get('/api/products/')
    # Checking last product first since response
    # is in descending order by created time
    assert response.data[0] == anydict({
        'name': product_last.name,
        'description': product_last.description,
        'url': reverse_url('product-detail', kwargs={'pk': product_last.pk}),
    })
    assert response.data[1] == anydict({
        'name': product_first.name,
        'description': product_first.description,
        'url': reverse_url('product-detail', kwargs={'pk': product_first.pk}),
    })


def test_product_retrieve(api_client, product_factory, anydict):
    product = product_factory()
    response = api_client.get(f'/api/products/{product.pk}/')
    assert response.data == anydict({
        'name': product.name,
        'description': product.description
    })


def test_product_update_or_delete_are_not_allowed(api_client, product_factory):
    product = product_factory()
    response = api_client.put(
        f'/api/products/{product.pk}/', {'name': 'New Name'})
    assert response.status_code == 405
    response = api_client.patch(
        f'/api/products/{product.pk}/', {'name': 'New Name'})
    assert response.status_code == 405
    response = api_client.delete(f'/api/products/{product.pk}/')
    assert response.status_code == 405
