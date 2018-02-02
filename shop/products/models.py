from django.db import models
from django.utils.translation import ugettext_lazy as _


class Product(models.Model):
    """
    Represents a product record.
    """
    name = models.CharField(_('name'), max_length=128)
    description = models.TextField(_('description'), blank=True)
    photo = models.ImageField(_('photo'), upload_to='products', null=True)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', 'name']

    def __str__(self):
        return f'{self.name} ${self.price}'
