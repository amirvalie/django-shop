# Generated by Django 4.0.7 on 2023-06-29 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=20, verbose_name='استان')),
                ('city', models.CharField(max_length=50, verbose_name='شهر')),
                ('address', models.TextField(verbose_name='ادرس')),
                ('post_code', models.CharField(max_length=10, verbose_name='کد پستی')),
                ('plaque', models.CharField(max_length=10, verbose_name='پلاک')),
                ('unit', models.CharField(max_length=10, verbose_name='واحد')),
                ('phone_number', models.CharField(max_length=11, verbose_name='شماره تلفن')),
                ('active_address', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'ادرس',
                'verbose_name_plural': 'ادرس ها',
            },
        ),
    ]