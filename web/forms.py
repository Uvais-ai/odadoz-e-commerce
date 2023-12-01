from django import forms
from django.utils.translation import gettext_lazy as _
from web.models import Contact
from django.forms import widgets


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ('timestamp',)
        widgets = {
            "name": widgets.TextInput(attrs={"class": "form_item", "placeholder" : "Your Name"}),
            "email": widgets.EmailInput(attrs={"class": "form_item", "placeholder": "Your Email"}),
            "subject": widgets.TextInput(attrs={"class": "form_item", "placeholder": "Your Subject"}),
            "message": widgets.Textarea(attrs={"class": "form_item", "placeholder": "Message"}),
        }