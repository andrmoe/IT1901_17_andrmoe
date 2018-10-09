from django.forms.models import modelform_factory
from django.forms import Textarea
from .models import Post


AuthorForm = modelform_factory(Post, fields=['title', 'body', 'needs_proofreading'],
                             widgets={'body': Textarea(attrs={'cols': 100, 'rows': 25})})

EditorForm = modelform_factory(Post, fields=['title', 'body', 'needs_proofreading', 'published', 'comment'],
                             widgets={'body': Textarea(attrs={'cols': 100, 'rows': 25})})
