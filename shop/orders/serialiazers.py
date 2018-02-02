from django.conf import settings
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        IntegerField, ModelSerializer)

from products.serializers import ProductSerializer

from .models import Cart, CartProduct


class CartProductSerializer(HyperlinkedModelSerializer):
    quantity = IntegerField(
        min_value=1, max_value=settings.ORDERS_CART_MAX_PRODUCTS_QUANTITY)

    class Meta:
        model = CartProduct
        exclude = ['cart']


class CartProductNestedSerializer(HyperlinkedModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        exclude = ['cart']


class CartSerializer(ModelSerializer):
    cart_products = CartProductNestedSerializer(
        source='get_cart_products', many=True, read_only=True)

    class Meta:
        model = Cart
        exclude = ['id', 'products', 'user']
