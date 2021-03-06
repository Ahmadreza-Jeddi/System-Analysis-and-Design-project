from django.db import models
from . import product, customer
from .driver import provinces

class ProductSubmit(models.Model):
    submitter = models.ForeignKey(to=customer.Customer,
                                  on_delete=models.CASCADE,
                                  verbose_name="فروشنده")
    product = models.ForeignKey(to=product.Product,
                                on_delete=models.CASCADE,
                                verbose_name="نوع محصول")
    active = models.BooleanField(verbose_name="محصول قابل خرید است",
                                 default=True)
    date = models.DateField(verbose_name="تاریخ ثبت", null=False)
    quantity = models.PositiveIntegerField(verbose_name="مقدار محصول", null=False)
    price = models.PositiveIntegerField(verbose_name="قیمت", null=False)
    province = models.CharField(max_length=30, choices=provinces, verbose_name="استان", null=False, default='fars')
    location = models.TextField(verbose_name="آدرس فروشنده", null=False)

    def __str__(self):
        fullname = self.submitter.first_name + " " +  self.submitter.last_name
        pr = self.product.name
        return pr + " توسط " + fullname

    def getProvince(self):
        for p in provinces:
            if self.province == p[0]:
                return p[1]
