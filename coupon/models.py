from django.db import models
from django.core.validators import MinValueValidator, \
MaxValueValidator
# Create your models here.


class Coupon(models.Model):
    code=models.CharField(max_length=50,verbose_name="کد")
    valid_from=models.DateTimeField(verbose_name="اعتبار از")
    valid_to=models.DateTimeField(verbose_name='اعتبار تا')
    discount=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],verbose_name="درصد تخفیف")
    active=models.BooleanField(verbose_name="فعال")

    class Meta:
        verbose_name='کد تخفیف'
        verbose_name_plural='کد تخفیف ها'

    def __str__(self) -> str:
        return self.code