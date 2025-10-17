from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

type= {
    1: _('Tea Wet'),
    2: _('Tea Dry'),
    3: _('Tea Leaves')
}
employeetype={
    1: _("Fixed Daily Worker"),
    2: _("Casual Worker")
}

phone_regex = RegexValidator(regex=r'^\+?\d{10,12}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(validators=[phone_regex], max_length=12,default="1234567890")
    employee_type= models.IntegerField(choices=employeetype, default=1)
    profile = models.ImageField(upload_to='profile/',blank=True, null=True)

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    name = models.CharField(max_length=255, default=None)
    purchase_no = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pay_status = models.BooleanField(default=False)
    type= models.IntegerField(choices=type, default=1)
    create_date = models.DateTimeField(auto_now_add=True)

class RecoveryPurchase(models.Model):
    delete_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delete_by')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchases_recory')
    name = models.CharField(max_length=255,  default="Default")
    purchase_no = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pay_status = models.BooleanField(default=False)
    type= models.IntegerField(choices=type, default=1)
    create_date = models.DateTimeField()
    delete_date = models.DateTimeField(auto_now_add=True)

class SaleProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saler')
    company_name = models.CharField(max_length=255, default=None)
    name = models.CharField(max_length=255, default=None)
    sale_no = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pay_status = models.BooleanField(default=False)
    type = models.IntegerField(choices=type, default=1)
    create_date = models.DateTimeField(auto_now_add=True)

class RecoverySaleProduct(models.Model):
    delete_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delete_by_sale')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='saler_by')
    company_name = models.CharField(max_length=255, default="Default")
    name = models.CharField(max_length=255)
    sale_no = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pay_status = models.BooleanField(default=False)
    type = models.IntegerField(choices=type, default=1)
    create_date = models.DateTimeField()
    delete_date = models.DateTimeField(auto_now_add=True)


class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    is_leave = models.BooleanField(default=False)
    paystatus = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Salary(models.Model):
    worklog = models.OneToOneField(WorkLog, on_delete=models.CASCADE, related_name='salary')
    amount= models.DecimalField(default=5000, max_digits=10, decimal_places=2)


