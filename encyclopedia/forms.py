from django import forms
from . import util


class SearchForm(forms.Form):
    query = forms.CharField(label="Search Encyclopedia", max_length=20)


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title:", max_length=50)
    content = forms.CharField(
        label="Content:",
        widget=forms.Textarea(
            attrs={
                "name": "content",
            }
        ),
    )


class EditPageForm(forms.Form):
    content = forms.CharField(
        label="Content:", widget=forms.Textarea(attrs={"name": "content"})
    )
