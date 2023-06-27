import datetime
from typing import Any
from django.urls.base import reverse_lazy
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, CreateView
from django.contrib.messages.views import SuccessMessageMixin

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import status

from news_check.models import Article
from news_check.serializer import ArticleSerializer
from news_check.forms import ArticleForm
from news_check.news_class_predict import predict_class


class ArticleListView(ListView):
    """Получение списка проверенных новостей"""

    model = Article
    context_object_name = 'articles'
    template_name = 'news_check/index.html'
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.all()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = ArticleForm
        return context


class ArticleCreateView(SuccessMessageMixin, CreateView):
    """Проверка статьи на достоверность"""
    
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('home')
    success_message = 'Новость проверена!'

    def get_success_message(self, cleaned_data):
        return self.success_message

    def form_valid(self, form):
        self.object = form.save(commit=False)
        predicted_class = predict_class(self.request.POST['text'])
        self.object.date = datetime.datetime.now()
        self.object.category = predicted_class

        self.object.save()
        return super(ArticleCreateView, self).form_valid(form)


class MyHTMLRenderer(TemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        data = super().get_template_context(data, renderer_context)
        if not data:
            return {}
        else:
            return data


class ArticleListAPIView(APIView):
    """Получение списка проверенных новостей"""

    def get(self, request):
        queryset = Article.objects.all()
        articles = ArticleSerializer(instance=queryset, many=True)
        
        return Response(
            {
                'articles': articles.data
            },
            status=status.HTTP_200_OK
        )


class ArticleCreateAPIView(CreateAPIView):
    """Проверка статьи на достоверность"""

    permission_classes = [AllowAny, IsAuthenticated]
    serializer_class = ArticleSerializer
    form_class = ArticleForm
    queryset = Article.objects.all()


    def post(self, request, *args, **kwargs):
        predicted_class = predict_class(request.data['text'])

        request.data._mutable=True
        request.data['category'] = predicted_class
        request.data['date'] = datetime.datetime.now()

        return super().post(request, *args, **kwargs)