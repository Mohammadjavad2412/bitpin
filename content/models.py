from django.db import models
from users.models import Users

class Post(models.Model):

    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    avg_score = models.FloatField(null=True, blank=True)
    std_score = models.FloatField(null=True, blank=True)
    total_score = models.IntegerField(null=True, blank=True)
    sum_of_squared_scores = models.IntegerField(null=True, blank=True)
    rate_count = models.IntegerField(null=True, blank=True)

class Score(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    rate = models.IntegerField(null=True, blank=True)
