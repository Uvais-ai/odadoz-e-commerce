from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Min
from django.shortcuts import render
from django.views.generic import DetailView
from django.core.paginator import Paginator
#model
from .models import Slider
from .models import Category
from .models import Product
from .models import Brand
#wishlist
from order.models import Wishlist
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sliders = Slider.objects.all()
        categories = Category.objects.all()
        products = Product.objects.all()
        best_sellers = Product.objects.filter(is_best_seller=True)[:8]
        our_product = Product.objects.filter(is_our_product=True)[:8]
        new_product = Product.objects.filter(is_new_product=True)[:8]
        hot_deal = Product.objects.filter(is_hot_deal=True)[:8]
        big_sale = Product.objects.filter(is_popular=True)[:8]

        if self.request.user.is_authenticated:
            wishlist_items = Wishlist.objects.filter(user=self.request.user)
            wishlist_items_count = wishlist_items.count()
        else:
            wishlist_items = []
            wishlist_items_count = 0

        context.update({
            'sliders': sliders,
            "categories": categories,
            'all_categories': Category.objects.all(),
            'best_sellers' : best_sellers,
            'our_product': our_product,
            'new_product': new_product,
            'hot_deal': hot_deal,
            'popular': big_sale,
            'wishlist_items_count': wishlist_items_count,
            "products": products,
        })
        return context
    

class ShopView(TemplateView):
    template_name = "shop.html"

    def get_context_data(self, **kwargs):
        
        categories = Category.objects.all()
        products = Product.objects.all()
        brands = Brand.objects.all()
        selected_category = None

        if self.request.user.is_authenticated:
            wishlist_items = Wishlist.objects.filter(user=self.request.user)
            wishlist_items_count = wishlist_items.count()
        else:
            wishlist_items = []
            wishlist_items_count = 0

        category_slug = self.request.GET.get('category')
        brand_ids = self.request.GET.getlist('brand')
        search = self.request.GET.get('query')
        sort_by = self.request.GET.get("sort_by")
        min_price = self.request.GET.get("min_price")  
        max_price = self.request.GET.get("max_price") 

        if category_slug:
            selected_category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(categories=selected_category)

        if brand_ids:
            products = products.filter(brands__slug__in=brand_ids)

        if search:   
            products = products.filter(name__icontains=search)

        if min_price is not None and max_price is not None:
            products = products.filter(price__gte=min_price, price__lte=max_price)

        if sort_by:
            if sort_by == "low_to_high":
                annotated_queryset = products.annotate(
                    min_price=Min("price")
                )
                products = annotated_queryset.order_by("min_price")
            elif sort_by == "high_to_low":
                annotated_queryset = products.annotate(
                    min_price=Min("price")
                )
                products = annotated_queryset.order_by("-min_price")
            elif sort_by == "rating":
                products = products.order_by("-rating")
            else:
                products = products.order_by("-id")

        write_name_ishtam = self.request.GET.get('filter', '*')
        if write_name_ishtam != '*':
            products = products.filter(
                **{write_name_ishtam: True}
            )

        paginator = Paginator(products, 8) 
        page_number = self.request.GET.get('page') 
        onefinal = paginator.get_page(page_number)
        total_pages = onefinal.paginator.num_pages  
    
        context = {
            "categories": categories,
            "products": onefinal,
            "selected_category": selected_category,
            'all_categories': Category.objects.all(),
            'brands': brands,
            'brand_ids': brand_ids,
            'wishlist_items_count': wishlist_items_count,
            'ishtam_view': write_name_ishtam,
            'post': onefinal, 
            'lastpage': total_pages,
            'totalpagelist': [n + 1 for n in range(total_pages)],
        }
        return context
    

# def index(request):
#     sliders = Slider.objects.all()
#     categories = Category.objects.all()
#     products = Product.objects.all()
#     best_sellers = Product.objects.filter(is_best_seller=True)[:8]
#     our_product = Product.objects.filter(is_our_product=True)[:8]
#     new_product = Product.objects.filter(is_new_product=True)[:8]
#     hot_deal = Product.objects.filter(is_hot_deal=True)[:8]
#     big_sale = Product.objects.filter(is_popular=True)[:8]
    
#     if request.user.is_authenticated:
#         wishlist_items = Wishlist.objects.filter(user=request.user)
#         wishlist_items_count = wishlist_items.count()
#     else:
#         wishlist_items = []
#         wishlist_items_count = 0

#     context = {
#         'sliders': sliders,
#         "categories": categories,
#         'all_categories': Category.objects.all(),
#         'best_sellers' : best_sellers,
#         'our_product': our_product,
#         'new_product': new_product,
#         'hot_deal': hot_deal,
#         'popular': big_sale,
#         'wishlist_items_count': wishlist_items_count,
#         "products": products,
#     }
#     return render(request, "index.html", context)


# def shop(request):
#     categories = Category.objects.all()
#     products = Product.objects.all()
#     brands = Brand.objects.all()
#     selected_category = None

#     if request.user.is_authenticated:
#         wishlist_items = Wishlist.objects.filter(user=request.user)
#         wishlist_items_count = wishlist_items.count()
#     else:
#         wishlist_items = []
#         wishlist_items_count = 0

#     category_slug = request.GET.get('category')
#     brand_ids = request.GET.getlist('brand')
#     search = request.GET.get('query')
#     sort_by = request.GET.get("sort_by")
#     min_price = request.GET.get("min_price")  
#     max_price = request.GET.get("max_price") 
    
#     if category_slug:
#         selected_category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(categories=selected_category)
#     if brand_ids:
#         products = products.filter(brands__slug__in=brand_ids)
#     if search:   
#         products = products.filter(name__icontains=search)
#     if min_price is not None and max_price is not None:
#         products = products.filter(price__gte=min_price, price__lte=max_price)
#     if sort_by:
#         if sort_by == "low_to_high":
#             annotated_queryset = products.annotate(
#                 min_price=Min("price")
#             )
#             products = annotated_queryset.order_by("min_price")
#         elif sort_by == "high_to_low":
#             annotated_queryset = products.annotate(
#                 min_price=Min("price")
#             )
#             products = annotated_queryset.order_by("-min_price")
#         elif sort_by == "rating":
#             products = products.order_by("-rating")
#         else:
#             products = products.order_by("-id")

#     write_name_ishtam = request.GET.get('filter', '*')
#     if write_name_ishtam != '*':
#         products = products.filter(
#             **{write_name_ishtam: True}
#         )
#     paginator = Paginator(products, 8) 
#     page_number = request.GET.get('page') 
#     onefinal = paginator.get_page(page_number)
#     total_pages = onefinal.paginator.num_pages  
    
#     context = {
#         "categories": categories,
#         "products": onefinal,
#         "selected_category": selected_category,
#         'all_categories': Category.objects.all(),
#         'brands': brands,
#         'brand_ids': brand_ids,
#         'wishlist_items_count': wishlist_items_count,
#         'ishtam_view': write_name_ishtam,
#         'post': onefinal, 
#         'lastpage': total_pages,
#         'totalpagelist': [n + 1 for n in range(total_pages)],
#     }
#     return render(request, "shop.html", context)


class ShopDetailView(DetailView):
    model = Product
    template_name = "shop_details.html"
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            wishlist_items = Wishlist.objects.filter(user=self.request.user)
            wishlist_items_count = wishlist_items.count()
        else:
            wishlist_items = []
            wishlist_items_count = 0
            
        context['request'] = self.request
        context['all_categories'] = Category.objects.all()
        context['wishlist_items_count'] = wishlist_items_count
        return context


def filter_data(request):
    brands = request.GET.getlist('brand[]')

    if brands:
        product = Product.objects.filter(brands__slug__in=brands).order_by('-id')
    else :
        product = Product.objects.all().order_by('-id')

    context  = {
        'products': product
    }
    t = render_to_string('ajax/shop.html', context)
    return JsonResponse({'data': t})




