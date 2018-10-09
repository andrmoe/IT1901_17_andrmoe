from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='author_of')
    editor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='editor_of', null=True)
    needs_proofreading = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    comment = models.TextField(null=True)

    def __str__(self):
        return self.title
