from django import forms

from .models import OrderInquiry


class OrderInquiryForm(forms.ModelForm):
    class Meta:
        model = OrderInquiry
        fields = ('customer_name', 'customer_phone', 'customer_email', 'notes')
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }