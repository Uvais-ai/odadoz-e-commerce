from django.shortcuts import render
from web.forms import ContactForm
from django.http import HttpResponse
import json
from product.models import Category
from order.models import Wishlist


# Create your views here.
def contact(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_items_count = wishlist_items.count()
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Message successfully updated",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
            }
        return HttpResponse(
            json.dumps(response_data), content_type="application/javascript"
        )
    else:
        context = {
            "form": form,
            'all_categories': Category.objects.all(),
            'wishlist_items_count': wishlist_items_count,
        }
    return render(request, "contact.html", context)


def about(request):
    return render(request, "about.html")


