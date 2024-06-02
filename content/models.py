from django.db import models
from users.models import Users

class Post(models.Model):

    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)


class Score(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    rate = models.IntegerField(null=True, blank=True)
    