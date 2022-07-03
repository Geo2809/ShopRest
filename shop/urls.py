from cgitb import lookup
from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)

router_products = routers.NestedDefaultRouter(router, 'products', lookup='product')
router_products.register('reviews', views.ReviewViewSet, basename='product-reviews')

router_carts = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
router_carts.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + router_products.urls + router_carts.urls