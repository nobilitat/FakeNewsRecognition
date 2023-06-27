from django import forms
from news_check.models import Article


class ArticleForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = (
            'text',
        )
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows': 6, 
                    'placeholder': 'Введите текст статьи'})
        }