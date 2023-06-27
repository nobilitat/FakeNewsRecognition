from django.db import models
import datetime
from news_check.choices import Categories


class Article(models.Model):
    """Описание свойств таблицы статьи"""

    title = models.CharField('Название статьи', max_length=400, blank=True, null=True)
    text = models.TextField('Текст статьи')
    date = models.DateTimeField('Дата анализа статьи', default=datetime.datetime.now())
    category = models.CharField(
        choices=Categories.choices, 
        verbose_name='Категория', 
        max_length=30, 
        blank=True, 
        null=True
    )    

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering=('-date',)
