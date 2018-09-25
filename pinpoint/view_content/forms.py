from django.forms.models import modelform_factory
from .models import Post


PostForm = modelform_factory(Post, fields='__all__')
