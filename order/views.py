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


# Create your views here.
@login_required(login_url="auth_login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("order:cart_detail")


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
    # Your existing logic to get wishlist items for the current user
    wishlist_items = Wishlist.objects.filter(user=request.user)

    # Count the number of wishlist items
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

        # Get form data
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        district = request.POST.get('district')
        address = request.POST.get('streetaddress')
        town = request.POST.get('town')
        country = request.POST.get('country')
        postcode = request.POST.get('postcode')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')

        # Check if required fields are not None
        if any(field is None for field in [firstname, lastname, district, address, town, country, postcode, email, telephone]):
            # Handle the case where required fields are not provided
            messages.error(request, "Please fill in all the required fields.")
            return redirect('product:index')

        # Create Order instance
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

        # Create Order_Item instances
        for i in cart:
            a = float(cart[i]['price'])
            b = int(cart[i]['quantity'])
            total = a * b

            product_name = cart[i]['name']

            # Retrieve the product instance based on the product name
            product = Product.objects.get(name=product_name)

            order_item = Order_Item(
                order=order_1,
                product=product,  # Use the product field instead of product_name
                product_name=product_name,
                image=cart[i]['image'],
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                total=total
            )
            order_item.save()


        # Clear the cart after the order is placed
        request.session['cart'] = {}

        messages.success(request, "Order placed successfully!")
        return redirect("product:index")

    return render(request, 'checkout/checkout.html')


def your_order(request):
    if request.user.is_authenticated:
        uid = request.user.id
        user = User.objects.get(id=uid)
        orders = Order.objects.filter(user=user)
        order_items = Order_Item.objects.filter(order__in=orders)
    else:
        # Handle the case when the user is not authenticated
        order_items = []

    context = {
        'order_items': order_items,
    }
    return render(request, 'order.html', context)


@login_required(login_url="auth_login")
def wishlist(request):
    # Your existing logic to get wishlist items for the current user
    wishlist_items = Wishlist.objects.filter(user=request.user)

    # Count the number of wishlist items
    wishlist_items_count = wishlist_items.count()

    # Your other context data
    context = {
        'wishlist_items': wishlist_items,
        'wishlist_items_count': wishlist_items_count,
        'all_categories': Category.objects.all(),
        # Other context data...
    }

    return render(request, 'wishlist.html', context)


@login_required(login_url="auth_login")
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is not already in the wishlist
    if not Wishlist.objects.filter(user=request.user, product=product).exists():
        wishlist_item = Wishlist(user=request.user, product=product, price=product.price)
        wishlist_item.save()
        messages.success(request, f"{product.name} added to your wishlist!")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")

    return redirect("product:index")


@login_required(login_url="auth_login")
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id)

    # Check if the user trying to remove the item is the owner
    if wishlist_item.user == request.user:
        wishlist_item.delete()
        messages.success(request, f"{wishlist_item.product.name} removed from your wishlist!")
    else:
        messages.error(request, "You are not authorized to remove this item from the wishlist.")

    return redirect("order:wishlist")









