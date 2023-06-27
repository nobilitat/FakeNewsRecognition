from django.contrib import admin
from news_check.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'date')

admin.site.register(Article, ArticleAdmin)
