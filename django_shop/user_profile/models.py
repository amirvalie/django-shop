from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Manager

User = get_user_model()


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    state = models.CharField(max_length=20, verbose_name='استان')
    city = models.CharField(max_length=50, verbose_name='شهر')
    address = models.TextField(verbose_name='ادرس')
    post_code = models.CharField(max_length=10, verbose_name='کد پستی')
    plaque = models.CharField(max_length=10, verbose_name='پلاک')
    unit = models.CharField(max_length=10, verbose_name='واحد')
    phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن')
    active_address = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Address, self).save(*args, **kwargs)

    def empty_field_address(self):
        """
        It checks if any field of the address model is empty and returns a false value.
        """
        for field in self._meta.fields:
            if not getattr(self, field.name):
                return False
        else:
            return True

    @classmethod
    def address_exists(cls, user_object):
        address = cls.objects.filter(user=user_object)
        if address.exists():
            return True
        return False

    class Meta:
        verbose_name = 'ادرس'
        verbose_name_plural = 'ادرس ها'
