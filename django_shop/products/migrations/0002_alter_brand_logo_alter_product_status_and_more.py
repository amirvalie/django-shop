# Generated by Django 4.0.7 on 2023-08-09 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=models.ImageField(upload_to='image/brands/logo/', verbose_name='لوگو'),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('d', 'پیش نویس'), ('p', 'انتشار')], default='d', max_length=1, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(upload_to='image/products/thumbnails/', verbose_name='عکس'),
        ),
        migrations.AlterField(
            model_name='specification',
            name='section',
            field=models.CharField(choices=[('both', 'هردو'), ('long_spec', 'توضیحات بلند'), ('short_spec', 'توضیحات کوتاه')], max_length=20, verbose_name='بخش'),
        ),
    ]
