from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Slider,
    Category,
    ProductImage,
    ProductBig_Sale,
    Product,
    Color,
    Brand,
)

# Register your models here.
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = (
        'brand_name',
        "image_preview",
    )
    prepopulated_fields = {"slug": ("brand_name",)}

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview", )
    prepopulated_fields = {"slug": ("name",)}
    search_fields=['name',]

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductBig_SaleInline(admin.TabularInline):
    model = ProductBig_Sale
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview", "categories",)
    list_filter = (
        "categories",
        "is_popular",
        "is_new_arrival",
        "is_best_seller",
        "is_our_product",
        "is_new_product",
        "is_hot_deal",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    inlines = [ProductImageInline, ProductBig_SaleInline]
    autocomplete_fields=['categories', 'brands',]

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name' , 'color_code')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name' ,)
    prepopulated_fields = {"slug": ("name",)}
    search_fields=['name',]