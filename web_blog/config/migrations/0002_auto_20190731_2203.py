# Generated by Django 2.2.3 on 2019-07-31 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidebar',
            name='display_type',
            field=models.PositiveIntegerField(choices=[(1, 'HTML'), (2, '最新文章'), (3, '最热文章'), (4, '最近评论'), (5, '个人分类')], default=1, verbose_name='展示类型'),
        ),
    ]
