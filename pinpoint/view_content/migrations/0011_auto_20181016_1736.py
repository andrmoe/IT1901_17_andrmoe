# Generated by Django 2.1.1 on 2018-10-16 15:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('view_content', '0010_category_subscribers'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='authorsubscription',
            unique_together={('subscriber', 'author')},
        ),
    ]
