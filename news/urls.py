from django.urls import path, include
# импортируем наше представление
from .views import PostsList, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostSearchView, PostCategoryView
from .views import SubscribeView, UnsubscribeView#, subscribe_to_category, unsubscribe_from_category

app_name = 'news'
urlpatterns = [
#   path('', MainView.as_view(), name='index'),
# path -- означает путь. В данном случае путь ко всем постам у нас останется пустым, позже станет ясно почему
    # т.к. PostsList сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('', PostsList.as_view(), name='newslist'), # name='posts' или 'news' или 'newslist' ?
    # pk -- это первичный ключ объекта, который будет выводиться у нас в шаблон
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'), # Ссылка на детали объекта (поста)
    path('add/', PostCreateView.as_view(), name='post_create'), # Ссылка на создание объекта (поста)
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_create'), # Ссылка на редактирование объекта (поста)
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'), # Ссылка на удаление объекта (поста)
    path('search/', PostSearchView.as_view(), name='post_search'), # Ссылка на страницу поиска объектов (постов)
    path('category/<int:pk>/', PostCategoryView.as_view(), name='category'),
    path('subscribe/<int:pk>/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<int:pk>/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('unsubscribe/<int:pk>/', UnsubscribeView.as_view(), name='unsubscribe'),
]
