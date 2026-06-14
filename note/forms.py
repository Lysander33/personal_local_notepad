from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "输入笔记标题...",
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 12,
                "placeholder": "输入笔记内容（支持 Markdown）...",
            }),
        }
        labels = {
            "title": "标题",
            "content": "内容",
        }


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
