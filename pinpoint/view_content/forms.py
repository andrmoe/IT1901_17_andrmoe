from django.forms.models import modelform_factory
from django.forms import Textarea
from django.forms import CheckboxSelectMultiple
from .models import Post


AuthorForm = modelform_factory(Post, fields=['title', 'body', 'categories', 'author'],
                               widgets={'title': Textarea(attrs={'cols': 100, 'rows': 1}),
                                        'body': Textarea(attrs={'cols': 100, 'rows': 25}),
                                        'categories': CheckboxSelectMultiple(),
                                        'author': CheckboxSelectMultiple()})


EditorForm = modelform_factory(Post, fields=['title', 'body', 'categories', 'comment'],
                               widgets={'title': Textarea(attrs={'cols': 100, 'rows': 1}),
                                        'body': Textarea(attrs={'cols': 100, 'rows': 25}),
                                        'categories': CheckboxSelectMultiple()})


ExEditorForm = modelform_factory(Post, fields=['title', 'body', 'published', 'categories', 'comment'],
                                 widgets={'title': Textarea(attrs={'cols': 100, 'rows': 1}),
                                          'body': Textarea(attrs={'cols': 100, 'rows': 25}),
                                          'categories': CheckboxSelectMultiple()})
