from django import forms
from project.models import Purchase
from project.serializers.generate_unique_key import generate_unique_sale_no
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['name', 'amount', 'price', 'total_price', 'pay_status', 'type']
        labels={'name': _("Name"), 'amount': _("Amount"), 'price': _("Price"), 'total_price': _("Total Price"), 'pay_status': _("Pay Status"), 'type': _("Type")}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Vendor/Supplier Name')}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': 'required',}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': 'required',}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01','required': 'required','readonly': 'readonly',}),
            'pay_status': forms.Select(attrs={'class': 'form-select'}, choices=[(True, _('Paid')), (False, _('Unpaid'))]),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 1:
            raise ValidationError(_("Amount must be at least 1."))
        return amount
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 1:
            raise ValidationError(_("Price must be at least 1."))
        return price
    
    def clean_total_price(self):
        total_price = self.cleaned_data.get('total_price')
        if total_price < 1:
            raise ValidationError(_("Total price must be at least 1."))
        return total_price
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if not instance.pk:
            instance.purchase_no = generate_unique_sale_no("PHNO", Purchase, 'purchase_no')
        if commit:
            instance.save()
        return instance