# Generated by Django 4.2 on 2023-04-27 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='photo',
            field=models.ImageField(default=0, upload_to=''),
        ),
    ]
