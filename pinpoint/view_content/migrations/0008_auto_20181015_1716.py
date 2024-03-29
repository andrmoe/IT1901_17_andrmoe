# Generated by Django 2.1.1 on 2018-10-15 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view_content', '0007_authorsubscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(to='view_content.Category'),
        ),
    ]
