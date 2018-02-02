from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    """
    Returns a list of all available products.

    retrieve:
    Get product instance details
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
