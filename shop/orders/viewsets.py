from django.conf import settings
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet

from .models import Cart, CartProduct
from .serialiazers import CartProductSerializer


class DuplicateError(ValidationError):
    status_code = status.HTTP_409_CONFLICT


class CartProductViewSet(ModelViewSet):
    """
    Returns a list of all cart products.

    retrieve:
    Get cart product instance details

    create:
    Create new cart product instance

    update:
    Update cart product instance details

    partial_update:
    Update cart product instance details partially

    delete:
    Delete cart product instance
    """
    serializer_class = CartProductSerializer

    def get_queryset(self):
        return CartProduct.objects.filter(cart__user_id=self.request.user.pk)

    def _validate_max_products(self, cart):
        max_number = settings.ORDERS_CART_MAX_PRODUCTS
        if cart.products.count() == max_number:
            message = _(
                'Maximum number of cart products exceeded (%(number)d).') % {
                    'number': max_number
                }
            raise ValidationError({'cart': [message]})

    def _validate_duplicate(self, cart, product):
        # Not the best way to handle unique together check,
        # decided do not use UniqueTogetherValidator since
        # it requires cart field to be not excluded.
        if CartProduct.objects.filter(cart=cart, product=product).exists():
            message = _('Duplicate entry')
            raise DuplicateError({'cart': [message], 'product': [message]})

    def perform_create(self, serializer):
        with transaction.atomic():
            cart = Cart.ensure_cart(self.request.user)
            product = serializer.validated_data['product']
            self._validate_max_products(cart)
            self._validate_duplicate(cart, product)
            serializer.save(cart=cart)
