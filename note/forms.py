from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """笔记表单"""

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
                "placeholder": "输入笔记内容...",
            }),
        }
        labels = {
            "title": "标题",
            "content": "内容",
        }
