# Generated by Django 4.2 on 2023-04-28 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_remove_review_ratings_remove_review_star_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='type',
            field=models.CharField(default='Filme', max_length=50),
        ),
    ]