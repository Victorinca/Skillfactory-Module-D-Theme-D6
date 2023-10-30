# import django_filters
# импортируем filterset, чем-то напоминающий знакомые дженерики
from django_filters import FilterSet, DateFilter, ModelChoiceFilter, CharFilter
from django import forms
from django.shortcuts import render
from .models import Post, Author, Category, PostCategory

# создаём фильтр для поиска объектов (постов)
class PostFilter(FilterSet):
    #postCreated = forms.DateField(field_name='postCreated', lookup_expr='date__gt', input_formats=['%d-%m-%Y'])
    postCreated = DateFilter(
        field_name='postCreated',
        lookup_expr='date__gt',
        label='Дата создания позже, чем',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'placeholder': 'дд.мм.гггг'
            }
        )
    )

    postTitle = CharFilter(
        field_name='postTitle',
        lookup_expr='icontains',
        label='Заголовок содержит'
    )

    postAuthor = ModelChoiceFilter(
        field_name='postAuthor',
        lookup_expr='exact',
        label='Никнейм автора',
        queryset=Author.objects.all()
    )

# Здесь в мета классе надо предоставить модель и указать поля,
# по которым будет фильтроваться (т.е. подбираться) информация о постах
    class Meta:
        model = Post
# поля, которые мы будем фильтровать (т.е. отбирать по каким-то критериям, имена берутся из моделей)
        fields = ('postCreated', 'postTitle', 'postAuthor')

# способ 1
#        fields = ('post_type', 'postCats', 'postRating', 'postAuthor', 'postCreated', 'postTitle', 'postText')
# способ 2
#        fields = {
#            'post_type': ['exact'], # Поле для работы с choices
#            'postCats': ['exact'], # Поле для работы с choices
#            'postRating': ['gt']  # больше, чем указал пользователь
#            'postAuthor': ['exact'], # Поле для работы с choices
#            'postCreated': ['date__gt'], # больше указаной даты
# Мы хотим, чтобы нам выводился заголовок, хотя бы отдалённо похожий на то, что запросил пользователь
#            'postTitle': ['icontains'],
#            'postText': ['icontains'], # Ищем по ключевым словам в тексте
#        }
