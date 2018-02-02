from rest_framework.generics import RetrieveDestroyAPIView

from .models import Cart
from .serialiazers import CartSerializer


class CartRetrieveDestroyView(RetrieveDestroyAPIView):
    """
    Get current cart instance details

    delete:
    Delete current cart instance
    """
    serializer_class = CartSerializer

    def get_object(self):
        return Cart.ensure_cart(self.request.user)
