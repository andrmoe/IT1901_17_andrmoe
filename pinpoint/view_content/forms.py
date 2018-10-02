from django.forms.models import modelform_factory
from .models import Post


PostForm = modelform_factory(Post, exclude=['date', 'author'])
