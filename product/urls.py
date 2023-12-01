from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("", views.index, name="index"),
    # shop
    path("shop", views.shop, name="shop"),
    path("shop/filter-data", views.filter_data, name="filter-data"),
    path('shop/<slug:slug>/', views.ShopDetailView.as_view(), name='shop_details'),
]