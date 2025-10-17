# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from project.models import UserProfile
from django.utils.translation import gettext_lazy as _

class UserForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=12,
        required=True,
        label=_("Phone"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':_('Enter Phone number')})
    )
    profile = forms.ImageField(
        label=_("Profile"),
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label=_("Password"),
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Enter password')})
    )
    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Enter Confirm password')})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_superuser']
        labels = {
            'username': _("Username"),
            'first_name': _("First name"),
            'last_name': _("Last name"),
            'email': _("Email address"),
            'is_staff': _("Staff"),
            'is_superuser': _("Superuser"),
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')}), 
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('First name'), 'required': 'required'}), 
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last name'), 'required': 'required'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email address'),'required': 'required'}), 
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}), 
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'})
            }

    default_error_messages = {
        'required': _("This field is required."),       
        'invalid': _("Invalid value."),                  
        'max_length': _("Ensure this value has at most %(limit_value)d characters (it has %(show_value)d)."),
        'min_length': _("Ensure this value has at least %(limit_value)d characters (it has %(show_value)d)."),
        'invalid_choice': _("Select a valid choice. That choice is not one of the available choices."),
        'unique': _("This value already exists."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            for key, message in self.default_error_messages.items():
                if key not in field.error_messages:
                    field.error_messages[key] = message

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)  # Ignore current user
        if qs.exists():
            raise ValidationError(_("This email is already registered!"))
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise ValidationError(_("Phone number must contain digits only."))
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password or confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', _("Passwords do not match!"))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        if password: 
            user.set_password(password)

        if commit:
            user.save()
            phone = self.cleaned_data.get('phone')
            profile = self.cleaned_data.get('profile')

            UserProfile.objects.update_or_create(
                user=user,
                defaults={'phone': phone, 'profile': profile}
            )
        return user

