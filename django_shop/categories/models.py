from django.db import models
from django.urls import reverse


# Create your models here.

class CategoryManager(models.Manager):
    def category_publish(self):
        return self.filter(status='p')


class CategoryABC(models.Model):
    STATUS_CHOICE = {
        ('p', 'انتشار'),
        ('d', 'پیش نویس'),
    }
    title = models.CharField(
        max_length=200,
        verbose_name='عنوان',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='ادرس دسته بندی'
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICE,
        verbose_name='وضعیت',
    )
    thumbnail = models.ImageField(
        upload_to='category',
        verbose_name='عکس',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class Category(CategoryABC):
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name='children',
        verbose_name="والد",
    )

    def get_absolute_url(self):
        return reverse('product:category_list', args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    objects = CategoryManager()


class Banner(CategoryABC):
    TYPE_CATEGORIES = {
        ('seasonal', 'فصلی'),
        ('special_offer', 'پیشنهادات ویژه')
    }
    description = models.CharField(
        max_length=250,
        verbose_name='توضیحات'
    )
    type_category = models.CharField(
        max_length=15,
        choices=TYPE_CATEGORIES,
        verbose_name='نوع دسته بندی'
    )

    def get_absolute_url(self):
        return reverse('product:banner', args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی ویژه'
        verbose_name_plural = 'دسته بندی های ویژه'

    objects = CategoryManager()
