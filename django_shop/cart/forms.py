from django import forms
from django.forms.widgets import HiddenInput
from django.utils.regex_helper import Choice

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductFrom(forms.Form):
    color = forms.CharField(max_length=50, required=False)
    size = forms.CharField(max_length=50, required=False)
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label="تعداد محصول")
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
