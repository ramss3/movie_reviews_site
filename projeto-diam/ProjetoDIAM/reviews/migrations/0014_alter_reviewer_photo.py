# Generated by Django 4.1.7 on 2023-04-30 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0013_rename_comments_review_avg_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewer',
            name='photo',
            field=models.CharField(default='/reviews/static/reviews/media/default.png', max_length=250),
        ),
    ]