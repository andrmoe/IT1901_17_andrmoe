from django.forms.models import modelform_factory
from django.forms import Textarea
from .models import Post


PostForm = modelform_factory(Post, fields=['title', 'body'], widgets={'body': Textarea(attrs={'cols': 100, 'rows': 100})})
