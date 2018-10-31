from django.forms.models import modelform_factory
from django.forms import Textarea
from django.forms import CheckboxSelectMultiple
from .models import Post
from django_select2.forms import HeavySelect2MultipleWidget
# from .views import get_group_members


AuthorForm = modelform_factory(Post, fields=['title', 'body', 'needs_proofreading', 'categories'],
                             widgets={'body': Textarea(attrs={'cols': 100, 'rows': 25}),
                                      'categories':CheckboxSelectMultiple(),})


EditorForm = modelform_factory(Post, fields=['title', 'body', 'needs_proofreading', 'needs_approval', 'categories', 'comment'],
                             widgets={'body': Textarea(attrs={'cols': 100, 'rows': 25}),
                                      'categories':CheckboxSelectMultiple()})


ExEditorForm = modelform_factory(Post, fields=['title', 'body','needs_proofreading', 'needs_approval', 'published', 'categories', 'comment'],
                             widgets={'body': Textarea(attrs={'cols': 100, 'rows': 25}),
                                      'categories':CheckboxSelectMultiple(),})
