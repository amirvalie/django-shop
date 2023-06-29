from django import forms
from django.db.models import fields
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['address']
        widgets = {'address': forms.HiddenInput()}        

class ChoicesForm(forms.Form):
    def __init__(self,obj_ids=None, *args, **kwargs):
        print('obj_ids',obj_ids)
        super(ChoicesForm, self).__init__(*args, **kwargs)
        self.fields['choice_field'].choices=obj_ids
        
    choice_field =forms.ChoiceField(choices=(),widget=forms.RadioSelect,required=True)