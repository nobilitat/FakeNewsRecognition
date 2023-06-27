from django.urls import path
from news_check.views import ArticleListView, ArticleCreateView, ArticleListAPIView, ArticleCreateAPIView
from rest_framework.documentation import include_docs_urls

API_ROUTE = 'api/v1/articles/'

urlpatterns = [
    path('', view=ArticleListView.as_view(), name='home'),
    path('create/', view=ArticleCreateView.as_view(), name='create_article'),
    
    path('docs/', include_docs_urls(title='Fake Recognition API')),
    path(f'{API_ROUTE}list', view=ArticleListAPIView.as_view()),
    path(f'{API_ROUTE}create', view=ArticleCreateAPIView.as_view())
]