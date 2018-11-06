from django.forms.models import modelform_factory
from django.forms import Textarea
from django.forms import CheckboxSelectMultiple
from .models import Post


AuthorForm = modelform_factory(Post, fields=['title', 'body', 'categories', 'author'],
                             widgets={'body': Textarea(attrs={'cols': 100, 'rows': 25}),
                                      'categories': CheckboxSelectMultiple(),
                                      'author': CheckboxSelectMultiple()})


EditorForm = modelform_factory(Post, fields=['title', 'body', 'categories', 'needs_proofreading', 'needs_approval', 'comment'],
                             widgets={'body': Textarea(attrs={'cols': 100, 'rows': 25}),
                                      'categories': CheckboxSelectMultiple()})


ExEditorForm = modelform_factory(Post, fields=['title', 'body', 'needs_proofreading', 'needs_approval', 'published', 'categories', 'comment'],
                             widgets={'body': Textarea(attrs={'cols': 100, 'rows': 25}),
                                      'categories': CheckboxSelectMultiple()})
