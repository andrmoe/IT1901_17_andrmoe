from django.db import models


class Post(models.Model):
    title = models.CharField(help_text="Title of the post.", max_length=200)
    body = models.TextField(help_text="content of the post.", )
    date = models.DateTimeField(help_text="Date the post was created.", auto_now_add=True)
    author = models.ManyToManyField('auth.User', help_text="Relation to the post's authors")
    editor = models.ForeignKey('auth.User', help_text="The editor assigned to this post.",  on_delete=models.CASCADE, related_name='editor_of', null=True)
    needs_proofreading = models.BooleanField(help_text="", default=False)
    published = models.BooleanField(help_text="", default=False)
    comment = models.TextField(help_text="", null=True)
    categories = models.ManyToManyField('Category', help_text="")
    saved_users = models.ManyToManyField('auth.User', help_text="",  related_name='users')
    needs_approval = models.BooleanField(help_text="", default=False)

    def __str__(self):
        return self.title


class AuthorSubscription(models.Model):
    subscriber = models.ForeignKey('auth.User', help_text="User subscribing to author", on_delete=models.CASCADE, related_name='subscribed_to')
    author = models.ForeignKey('auth.User', help_text="", on_delete=models.CASCADE, related_name='subscriber')

    class Meta:
        unique_together = ('subscriber', 'author')

    def __str__(self):
        return self.subscriber.username + " is subscribed to " + self.author.username


class Category(models.Model):
    name = models.CharField(help_text="", max_length=100)
    subscribers = models.ManyToManyField('auth.User', help_text="")

    def __str__(self):
        return self.name


class RoleRequest(models.Model):
    group = models.ForeignKey('auth.Group', help_text="The role being requested", on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', help_text="The user requesting the role", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' is requesting the role: ' + self.group.name
