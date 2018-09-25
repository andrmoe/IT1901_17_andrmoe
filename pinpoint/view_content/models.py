from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
