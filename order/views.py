from django.shortcuts import render, redirect
from product.models import Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User
from .models import Order,Order_Item
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Wishlist
from product.models import Category
from .models import UserProfile
from django.http import JsonResponse


# Create your views here.
@login_required(login_url="auth_login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("product:index")


@login_required(login_url="auth_login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("order:cart_detail")


@login_required(login_url="auth_login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("order:cart_detail")


@login_required(login_url="auth_login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("order:cart_detail")


@login_required(login_url="auth_login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("order:cart_detail")


@login_required(login_url="auth_login")
def cart_detail(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_items_count = wishlist_items.count()

    context = {
        'wishlist_items_count': wishlist_items_count,
        'all_categories': Category.objects.all(),
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url="auth_login")
def checkout(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        district = request.POST.get('district')
        address = request.POST.get('streetaddress')
        town = request.POST.get('town')
        country = request.POST.get('country')
        postcode = request.POST.get('postcode')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')

        if any(field is None for field in [firstname, lastname, district, address, town, country, postcode, email, telephone]):
            messages.error(request, "Please fill in all the required fields.")
            return redirect('product:index')

        order_1 = Order(
            user=user,
            firstname=firstname,
            lastname=lastname,
            district=district,
            address=address,
            town=town,
            country=country,
            postcode=postcode,
            email=email,
            telephone=telephone,
        )
        order_1.save()

        for i in cart:
            a = float(cart[i]['price'])
            b = int(cart[i]['quantity'])
            total = a * b

            product_name = cart[i]['name']
            product = Product.objects.get(name=product_name)
            order_item = Order_Item(
                order=order_1,
                product=product,  
                product_name=product_name,
                image=product.image, 
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                total=total
            )
            order_item.save()

        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")
        return redirect("product:index")
    
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_items_count = wishlist_items.count()
    
    context = {
        'wishlist_items': wishlist_items,
        'wishlist_items_count': wishlist_items_count,
        'all_categories': Category.objects.all(),
    }
    return render(request, 'checkout/checkout.html', context)


@login_required(login_url="auth_login")
def your_order(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_items_count = wishlist_items.count()

    if request.user.is_authenticated:
        uid = request.user.id
        user = User.objects.get(id=uid)
        orders = Order.objects.filter(user=user)
        order_items = Order_Item.objects.filter(order__in=orders)
    else:
        order_items = []

    context = {
        'order_items': order_items,
        'all_categories': Category.objects.all(),
        'wishlist_items_count': wishlist_items_count,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'order.html', context)


@login_required(login_url="auth_login")
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_items_count = wishlist_items.count()

    context = {
        'wishlist_items': wishlist_items,
        'wishlist_items_count': wishlist_items_count,
        'all_categories': Category.objects.all(),
    }
    return render(request, 'wishlist.html', context)


@login_required(login_url="auth_login")
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not Wishlist.objects.filter(user=request.user, product=product).exists():
        wishlist_item = Wishlist(user=request.user, product=product, price=product.price)
        wishlist_item.save()
        messages.success(request, f"Item added to your wishlist successfully!")
    else:
        messages.info(request, f"Item is already in your wishlist.")

    if request.is_ajax():
        return JsonResponse({'message': 'Item added to wishlist successfully'})

    return redirect("product:index")



@login_required(login_url="auth_login")
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id)

    if wishlist_item.user == request.user:
        wishlist_item.delete()
        messages.success(request, f"removed from your wishlist!")
    else:
        messages.error(request, "You are not authorized to remove this item from the wishlist.")

    return redirect("order:wishlist")


@login_required(login_url="auth_login")
def account(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_items_count = wishlist_items.count()

    context = {
        'wishlist_items': wishlist_items,
        'wishlist_items_count': wishlist_items_count,
        'all_categories': Category.objects.all(),
    }
    return render(request, 'account.html', context)


@login_required(login_url="auth_login")
def profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_items_count = wishlist_items.count()


    context = {
        'user_profile': user_profile,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': wishlist_items_count,
    }
    return render(request, 'profile.html', context)


@login_required(login_url="auth_login")
def profile_update(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()

    if request.method == 'POST':
        # Update other fields
        user_profile.first_name = request.POST.get('first_name', '')
        user_profile.last_name = request.POST.get('last_name', '')
        user_profile.bio_data = request.POST.get('bio_data', '')
        user_profile.email = request.POST.get('email', '')

        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            user_profile.profile_pic = profile_pic

        user_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('order:profile')

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'profile.html', context)
