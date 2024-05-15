from django.db import models
from django.utils import timezone
from six import string_types
import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class Review(models.Model):
    review_title = models.CharField(max_length=200)
    pub_data = models.IntegerField(default=2023)
    photo = models.CharField(max_length=500)
    overview = models.CharField(max_length=1000, default='')
    avg_rating = models.IntegerField(default=0)

    def str(self):
        return self.review_title

class Reviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.CharField(max_length=250, default="/static/reviews/media/default.png")
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

class Comment(models.Model):
    comment_text = models.CharField(max_length=500)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    pub_data = models.DateTimeField('data de publicacao')
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, default=None)

    def str(self):
        return self.comment_text

class Gender(models.Model):
    gender_category = models.CharField(max_length=100)
    reviews = models.ManyToManyField(Review)

    def str(self):
        return self.gender_category

class Rating(models.Model):
    rating_number = models.IntegerField(default=0, validators=[MaxValueValidator(5)])
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, default=None)

    def str(self):
        return self.rating_number
