from django.db import models

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

    def avg_rates(self,obj_id):
        return(
            self.annotate(
                avg=Avg('rates__rate')
            ).values_list('avg',flat=True).get(id=obj_id)
        )

    def count_rates(self,obj_id):
        return(
            self.annotate(
                count=Count('rates')
            ).values_list('count',flat=True).get(id=obj_id)
        )



class CategoryManager(models.Manager):
    def category_publish(self):
        return self.filter(status='p')


class CategoryABC(models.Model):
    STATUS_CHOICE={
        ('p','انتشار'),
        ('d','پیش نویس'),
    }
    title=models.CharField(
        max_length=200,
        verbose_name='عنوان',
    )
    slug=models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='ادرس دسته بندی'
    )
    status=models.CharField(
        max_length=1,
        choices=STATUS_CHOICE,
        verbose_name='وضعیت',
    )
    thumbnail=models.ImageField(
        upload_to='category',
        verbose_name='عکس',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class Product(models.Model):
    STATUS_CHOICE={
        ('p','انتشار'),
        ('d','پیش نویس'),
    }
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        verbose_name = 'مدیر'
    )
    title = models.CharField(
        max_length = 100,
        verbose_name = 'عنوان',
    )
    slug  = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='ادرس محصول',
    )
    main_category = models.ManyToManyField(
        MainCategory,
        verbose_name = 'دسته ها',
        related_name = 'products_for_category',
    )
    banner = models.ManyToManyField(
        SpecialCategory,
        verbose_name = 'بنرها',
        related_name = 'products_for_banner',
        blank = True,
    )
    brand = models.ForeignKey(
        Brand,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        related_name = 'products',
    )
    introduction = models.TextField(
        verbose_name = 'معرفی محصول',
        blank = True,
        null = True,
    )
    price = models.FloatField(
        verbose_name='قیمت واقعی محصول',
    )
    discount_product = models.ForeignKey(
        DiscountProduct,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        verbose_name = 'تخفیف محصول',
    )
    thumbnail = models.ImageField(
        upload_to = 'image',
        verbose_name  ='عکس',
    )
    created = models.DateTimeField(
        auto_now_add = True,
        verbose_name = 'زمان ساخت',
    )
    updated = models.DateField(
        auto_now = True,
        verbose_name = 'زمان تغییر',
    )
    status=models.CharField(
        max_length = 1,
        default = 'd',
        choices = STATUS_CHOICE,
        verbose_name = 'وضعیت'
    )
    quantity = models.IntegerField(
        verbose_name = 'تعداد محصولات',
    )
    available = models.BooleanField(
        default = True,
        verbose_name = 'موجود بودن محصول',
    ) 
    visits = models.ManyToManyField(
        IpAddress,
        related_name = 'product',
        verbose_name = 'تعداد بازدید ها',
        blank=True,
    )
    sales_number=models.IntegerField(
        default = 0,
        verbose_name = 'تعداد فروش',
    )



    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse(
            'product:product_detail',
            args=[self.slug],
        )

    def available_product(self):
        product_number=self.quantity - self.sales_number
        return True if product_number > 0 else False


    def valid_discount(self):
        discount_obj=self.discount_product
        if discount_obj is None:
            return False
        else:
            if discount_obj.valid_from < timezone.now() and discount_obj.valid_to > timezone.now():
                return True

    def cal_discount(self):
        discount_obj=self.discount_product
        discount=discount_obj.discount_percent if discount_obj else None
        if discount:
            percent=discount/100
            multiple=self.price * percent
            return self.price - multiple
        return discount
    cal_discount.short_description='قیمت با تخفیف'

    class Meta:
        verbose_name='محصول'
        verbose_name_plural='محصولات'
        ordering=['-created']
    objects=ProductManager()
