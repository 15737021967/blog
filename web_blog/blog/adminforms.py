from django import forms
from .models import Category, Tag, Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from  ckeditor.widgets import CKEditorWidget
# from dal import autocomplete


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label="摘要", required=False)

    class Meta:
        model = Post
        fields = (
            'category', 'tag', 'title', 'desc',
            'content', 'status', 'pro_category',
        )

    def clean(self):
        content = self.cleaned_data.get('content')
        if not content:
            self.add_error('content', "必须填此项！")
            return
        self.cleaned_data['content'] = content
        return super().clean()
