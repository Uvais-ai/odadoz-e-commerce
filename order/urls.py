from django.urls import path
from . import views
from .views import wishlist, add_to_wishlist, remove_from_wishlist

app_name = "order"

urlpatterns = [
    #cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('checkout',views.checkout,name='checkout'),
    path('order/',views.your_order,name='order'),
    # wishlist
    path('wishlist/', wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]

