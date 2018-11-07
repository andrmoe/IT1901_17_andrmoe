from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ManyToManyField('auth.User')
    editor = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='editor_of', null=True)
    needs_proofreading = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    comment = models.TextField(null=True)
    categories = models.ManyToManyField('Category')
    saved_users = models.ManyToManyField('auth.User', related_name='users')
    needs_approval = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class AuthorSubscription(models.Model):
    subscriber = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='subscribed_to')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='subscriber')

    class Meta:
        unique_together = ('subscriber', 'author')

    def __str__(self):
        return self.subscriber.username + " is subscribed to " + self.author.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    subscribers = models.ManyToManyField('auth.User')

    def __str__(self):
        return self.name


class RoleRequest(models.Model):
    group = models.ForeignKey('auth.Group', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' is requesting the role: ' + self.group.name
