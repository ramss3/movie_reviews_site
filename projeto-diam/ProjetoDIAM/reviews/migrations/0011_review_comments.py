# Generated by Django 4.1.7 on 2023-04-29 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_remove_review_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='comments',
            field=models.IntegerField(default=0),
        ),
    ]