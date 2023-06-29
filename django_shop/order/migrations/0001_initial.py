# Generated by Django 4.0.7 on 2023-06-29 13:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_shop.order.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatePikcer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ')),
                ('time_range', models.CharField(max_length=50, verbose_name='بازه زمانی')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='ساخت شده')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='بروز رسانی شده')),
                ('status', models.CharField(choices=[('failed', 'ناموفق'), ('returned', 'بازگشت داده شد'), ('unpaid', 'پرداخت نشده'), ('sending', 'درحال ارسال'), ('delivered', 'تحویل')], default='unpaid', max_length=15, verbose_name='وضعیت')),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارشات',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='قیمت')),
                ('total_price', models.FloatField(default=1, verbose_name='قیمت کل')),
                ('color', models.CharField(blank=True, max_length=50, null=True, verbose_name='رنگ')),
                ('size', models.CharField(blank=True, max_length=50, null=True, verbose_name='سایز')),
                ('quantity', models.IntegerField(default=1, verbose_name='تعداد')),
                ('product_arrival_time', models.DateField(default=django.utils.timezone.now)),
                ('issue_tracking', models.CharField(default=django_shop.order.models.gen_issue_traking, max_length=36)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='order.order', verbose_name='سفارش')),
            ],
            options={
                'verbose_name': 'کالا',
                'verbose_name_plural': 'کالاها',
            },
        ),
    ]
