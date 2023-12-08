from django.urls import path
from . import views
from .views import IndexView, ShopView

app_name = "product"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("shop/", ShopView.as_view(), name="shop"),
    path("shop/filter-data", views.filter_data, name="filter-data"),
    path('shop/<slug:slug>/', views.ShopDetailView.as_view(), name='shop_details'),
]