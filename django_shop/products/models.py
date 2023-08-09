from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count, Avg, Max
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django_shop.categories.models import Category
from django_shop.categories.models import Banner
from django.urls import  reverse
User=get_user_model()

# Create your models here.


class ProductManager(models.Manager):
    def product_publish(self):
        return self.filter(status='p')

    def discounted_products(self):
        return self.product_publish().filter(
            discount_product__valid_from__lte=timezone.now(),
            discount_product__valid_to__gte=timezone.now()
        )

    def number_of_visits(self):
        return self.product_publish().annotate(
            count=Count('visits')
        )

    def product_sales(self):
        return self.product_publish().annotate(
            max_sales_number=Max('sales_number')
        )

    def avg_rates(self, obj_id):
        return (
            self.annotate(
                avg=Avg('rates__rate')
            ).values_list('avg', flat=True).get(id=obj_id)
        )

    def count_rates(self, obj_id):
        return (
            self.annotate(
                count=Count('rates')
            ).values_list('count', flat=True).get(id=obj_id)
        )


class Brand(models.Model):
    brand_name=models.CharField(max_length = 100,unique=True,verbose_name='نام برند')
    logo = models.ImageField(upload_to='image/brands/logo/',max_length=100,verbose_name='لوگو')
    class Meta:
        verbose_name='برند'
        verbose_name_plural='برندها'

    def display_logo(self):
        logo_format=format_html(
            f'<image style="width:100px" src="{self.logo.url}">'
        )
        return logo_format

    def __str__(self):
        return self.brand_name


class Color(models.Model):
    code = models.CharField(
        max_length=50,
        verbose_name='کد رنگ',
    )
    name = models.CharField(max_length=50, verbose_name='نام رنگ')

    def __str__(self):
        return self.name

    def color_pic(self):
        return format_html(
            f'<p style="color:{self.code};width:200px;border:solid;border-width:10px;"></p>'
        )

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'

    color_pic.short_description = 'رنگ'


class Size(models.Model):
    size = models.CharField(
        max_length=150
    )

    class Meta:
        verbose_name = 'اندازه'
        verbose_name_plural = 'اندازه ها'

    def __str__(self):
        return self.size


class IpAddress(models.Model):
    ip = models.GenericIPAddressField()

    def __str__(self):
        return str(self.ip)


class DiscountProduct(models.Model):
    discount_percent=models.IntegerField(
        validators=[MinValueValidator(0),MaxValueValidator(100)],verbose_name="درصد تخفیف"
    )
    valid_from=models.DateTimeField(
        verbose_name="اعتبار از"
    )
    valid_to=models.DateTimeField(
        verbose_name='اعتبار تا'
    )
    active=models.BooleanField(
        verbose_name="فعال"
    )

    class Meta:
        verbose_name='تخفیف محصول'
        verbose_name_plural='تخفیف محصولات'

    def __str__(self):
        return str(self.discount_percent) + 'درصد'


class Product(models.Model):
    STATUS_CHOICE = {
        ('p', 'انتشار'),
        ('d', 'پیش نویس'),
    }
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='مدیر'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='عنوان',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='ادرس محصول',
    )
    category = models.ManyToManyField(
        Category,
        verbose_name='دسته ها',
        related_name='category_products',
    )
    banner = models.ManyToManyField(
        Banner,
        verbose_name='بنرها',
        related_name='banner_products',
        blank=True,
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='products',
    )
    introduction = models.TextField(
        verbose_name='معرفی محصول',
        blank=True,
        null=True,
    )
    price = models.FloatField(
        verbose_name='قیمت واقعی محصول',
    )
    discount_product = models.ForeignKey(
        DiscountProduct,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='تخفیف محصول',
    )
    thumbnail = models.ImageField(
        upload_to='image/products/thumbnails/',
        verbose_name='عکس',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ساخت',
    )
    updated = models.DateField(
        auto_now=True,
        verbose_name='زمان تغییر',
    )
    status = models.CharField(
        max_length=1,
        default='d',
        choices=STATUS_CHOICE,
        verbose_name='وضعیت'
    )
    quantity = models.IntegerField(
        verbose_name='تعداد محصولات',
    )
    available = models.BooleanField(
        default=True,
        verbose_name='موجود بودن محصول',
    )
    visits = models.ManyToManyField(
        IpAddress,
        related_name='product',
        verbose_name='تعداد بازدید ها',
        blank=True,
    )
    sales_number = models.IntegerField(
        default=0,
        verbose_name='تعداد فروش',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'product:product_detail',
            args=[self.slug],
        )

    def available_product(self):
        product_number = self.quantity - self.sales_number
        return True if product_number > 0 else False

    def valid_discount(self):
        discount_obj = self.discount_product
        if discount_obj is None:
            return False
        else:
            if discount_obj.valid_from < timezone.now() and discount_obj.valid_to > timezone.now():
                return True

    def cal_discount(self):
        discount_obj = self.discount_product
        discount = discount_obj.discount_percent if discount_obj else None
        if discount:
            percent = discount / 100
            multiple = self.price * percent
            return self.price - multiple
        return discount

    cal_discount.short_description = 'قیمت با تخفیف'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created']

    objects = ProductManager()


class Specification(models.Model):
    SECTION={
        ('short_spec','توضیحات کوتاه'),
        ('long_spec','توضیحات بلند'),
        ('both','هردو'),
    }
    product = models.ForeignKey(
            Product,
            on_delete=models.CASCADE,
            verbose_name='محصول',
            related_name='spec'
        )
    key=models.CharField(
            max_length=50,
            verbose_name='ویژگی'
        )
    value=models.CharField(
            max_length=150,
            verbose_name='مقدار ویژگی'
        )
    section=models.CharField(
            max_length=20,
            choices=SECTION,
            verbose_name='بخش'
        )

class ProductImage(models.Model):
    product=models.ForeignKey(
            Product,
            on_delete=models.CASCADE,
            verbose_name='محصول',
            related_name='product_image'
        )
    image=models.FileField(
            upload_to='image',
            verbose_name='عکس'
        )

    class Meta:
        verbose_name='عکس'
        verbose_name_plural='عکس ها'

class ProductColor(models.Model):
    product = models.ForeignKey(
            Product,
            on_delete=models.CASCADE,
            verbose_name='محصول',
            related_name='colors',
        )
    color = models.ForeignKey(
            Color,
            on_delete=models.CASCADE,
            verbose_name='رنگ محصول',
        )
    price = models.FloatField(
            verbose_name='قیمت رنگ محصول'
        )

class ProductSize(models.Model):
    product = models.ForeignKey(
            Product,
            on_delete=models.CASCADE,
            verbose_name='محصول',
            related_name='sizes',
        )
    size = models.ForeignKey(
            Size,
            on_delete=models.CASCADE,
            verbose_name='اندازه محصول',
        )
    price = models.FloatField(
            verbose_name='قیمت اندازه محصول',
        )

