from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Cart(models.Model):
    """
    Represents a shopping cart record.
    """
    user = models.OneToOneField(
        'auth.User', related_name='cart', on_delete=models.CASCADE)
    products = models.ManyToManyField(
        'products.Product', through='CartProduct', verbose_name=_('products'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Open cart #{self.pk}'

    def get_cart_products(self):
        """
        Returns a list of associated with a current cart CartProduct instances,
        joining products table to avoid N+1 queries in nested serializer.
        """
        return self.cart_products.select_related('product')

    @classmethod
    def ensure_cart(self, user):
        """
        Returns cart instance for a given user.
        If it does not exist - it will be created.
        """
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart


class CartProduct(models.Model):
    """
    Represents product to cart relation record.
    """
    QUANTITY_EXCEEDED_ERROR_MESSAGE = _(
        'You can add only %(quantity)s items of the same product' % {
            'quantity': settings.ORDERS_CART_MAX_PRODUCTS_QUANTITY
        })

    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, verbose_name=_('cart'),
        related_name='cart_products')
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE, verbose_name=_('product'))
    quantity = models.PositiveIntegerField(
        _('quantity'), validators=[MaxValueValidator(
            settings.ORDERS_CART_MAX_PRODUCTS_QUANTITY,
            message=QUANTITY_EXCEEDED_ERROR_MESSAGE)])

    class Meta:
        unique_together = ('cart', 'product')
