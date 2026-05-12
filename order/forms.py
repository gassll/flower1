from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('course_name', 'start_date', 'payment_method')
