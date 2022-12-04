from django.forms import ModelForm
from .models import Post
from django import forms


class PostCreationForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ['owner', 'title']
        widgets = {

            'content': forms.Textarea()
        }

    def __init__(self, *args, **kwargs):
        super(PostCreationForm, self).__init__(*args, **kwargs)

        self.fields['content'].widget.attrs.update(
            {'placeholder': 'What you are thinking...'})
        # for name, field in self.fields.items():
        #     field.widget.attrs.update({'class': 'input'})
