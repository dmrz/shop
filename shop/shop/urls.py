from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from core.views import FrontendLoginView, FrontendView
from orders.views import CartRetrieveDestroyView
from orders.viewsets import CartProductViewSet
from products.viewsets import ProductViewSet

router = DefaultRouter()
router.register(r'cart/products', CartProductViewSet, base_name='cartproduct')
router.register(r'products', ProductViewSet)


urlpatterns = [
    # API
    url(r'^api/auth/', include('rest_framework.urls')),
    url(r'^api/cart/$', CartRetrieveDestroyView.as_view()),
    url(r'^api/', include(router.urls)),
    url(r'^docs/', include_docs_urls(title='Shop API', public=False)),

    # Admin
    path('admin/', admin.site.urls),

    # Login/Logout
    url(r'^login/$', FrontendLoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]

# Media files
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    # Frontend (placed in the end to catch all the pathes by Vue.js app)
    url(r'^', FrontendView.as_view(), name='frontend')
]
