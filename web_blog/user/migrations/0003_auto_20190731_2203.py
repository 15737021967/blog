# Generated by Django 2.2.3 on 2019-07-31 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190723_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='address',
            field=models.CharField(blank=True, default='未知', max_length=50, null=True, verbose_name='地址'),
        ),
    ]