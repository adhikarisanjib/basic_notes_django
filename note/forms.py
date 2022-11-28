from dataclasses import fields
from django import forms

from note.models import Note

class NoteForm(forms.ModelForm):
    body = forms.Textarea()

    class Meta:
        model = Note
        fields = ['title', 'body']

