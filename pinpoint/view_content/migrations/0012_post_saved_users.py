# Generated by Django 2.1.1 on 2018-10-30 15:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('view_content', '0011_auto_20181016_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='saved_users',
            field=models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
