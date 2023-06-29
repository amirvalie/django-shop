from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, \
    MaxValueValidator
from ..products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()
from django.utils.timezone import now


# Create your models here.


class Rate(models.Model):
    rate = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    verbose_name = 'امتیاز'
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE, verbose_name='محصول',
        related_name='rates',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='کاربر'
    )
    date_added = models.DateTimeField(default=now, editable=False)
    date_changed = models.DateTimeField(default=now, editable=False)

    def save(self, *args, **kwargs):
        self.date_changed = now()
        super(Rate, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.rate)

    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازها'
