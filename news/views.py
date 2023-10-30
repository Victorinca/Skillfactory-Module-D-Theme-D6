from django.shortcuts import render, reverse, redirect
from django.utils import timezone
from datetime import datetime
from django.urls import reverse_lazy
#from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# импортируем необходимые дженерики
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# импортируем класс, говорящий о том, что в этом представлении будем выводить список объектов из БД
from django.views.generic import TemplateView
from django.views import View

#from django.core.paginator import Paginator
from django_filters.views import FilterView
from .models import Author, Category, Post, PostCategory, Comment, Subscription, SubscriptionCategory
from django.contrib.auth.models import User
# импортируем недавно написанный фильтр
from .filters import PostFilter
#from .filters import CategoryFilter
# импортируем нашу форму
from .forms import PostForm
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.core.mail import send_mail
from django.core.mail import mail_admins # импортируем функцию для массовой отправки писем админам
from django.core.mail import mail_managers

from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import QuerySet
import smtplib
import ssl


# Create your views here.
class PostsList(ListView):
# указываем модель, объекты которой мы будем выводить
    model = Post
# указываем имя шаблона, в котором будет лежать HTML,
# в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    template_name = 'news/newslist.html'
# далее имя списка (по заданию нужно 'news'), в котором будут лежать все объекты,
# его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    context_object_name = 'news'
# сортировка по id в порядке убывания
#    queryset = Post.objects.all().order_by('-id')
# вывод объектов в обратном порядке, начиная с последнего созданного объекта
#    queryset = Post.objects.all().order_by('-postCreated')
# или можно так - вывод объектов в обратном порядке, начиная с последнего созданного объекта
    ordering = ['-postCreated']
#    paginate_by = 2 # поставим постраничный вывод в 2 элемента
    paginate_by = 10 # поставим постраничный вывод в 10 элементов
#    filterset_class = PostFilter

    # def get_queryset(self) -> QuerySet(any):
    #     post_filter = PostFilter(self.request.GET, queryset=Post.objects.all())
    #     return post_filter.qs.order_by('-dateCreation')

# метод get_context_data нужен нам для того, чтобы передать переменные в шаблон.
# В возвращаемом словаре context будут храниться все переменные.
# Ключи этого словаря и есть переменные, к которым можно потом обратиться через шаблон.
    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (полиморфизм)
        context = super().get_context_data(**kwargs)
        #context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        user = self.request.user
        if user.is_authenticated:
            news = context['news']
            for post in news:
                post.postCats.all()
                post.categories = [{'category': cat, 'is_subscribed': cat.subscribers.filter(email=user.email).exists()}
                                   for cat in post.postCats.all()]
            context['user'] = user
        else:
        # Действия, если пользователь не авторизован
        # Например, перенаправление на страницу входа или отображение сообщения об ошибке
            news = context['news']
            for post in news:
                post.postCats.all()
                post.categories = [{'category': cat} for cat in post.postCats.all()]
        return context


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid(): # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый пост
            form.save()

# дженерик для получения деталей об объекте (посте)
# создаём представление, в котором будут детали конкретного отдельного поста
class PostDetailView(DetailView):
# модель всё та же, но мы хотим получать детали конкретно отдельного поста
    template_name = 'news/post_detail.html' # вместо шаблона post.html, сделаем post_detail.html
    queryset = Post.objects.all()

# дженерик для создания объекта.
# Надо указать только имя шаблона и класс формы. Остальное он сделает за нас
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', 'news.change_post')
    template_name = 'news/post_create.html'
    form_class = PostForm

    def create_post(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save()
                form.send_mail(post)
                # redirect or render
        else:
            form = PostForm()
        return render(request, 'create_post.html', {'form': form})

# дженерик для редактирования объекта
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'news/post_create.html'
    form_class = PostForm

    # метод get_object используем вместо queryset, чтобы получить информацию об объекте, который собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

# дженерик для удаления объекта
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:newslist') # не забываем импортировать функцию reverse_lazy из пакета django.urls

# дженерик для страницы поиска постов
class PostSearchView(FilterView):
    model = Post
    context_object_name = 'posts'
    template_name = 'news/post_search.html'
    queryset = Post.objects.all().order_by('-postCreated')
    filterset_class = PostFilter

# дженерик для страницы какой-либо категории
class PostCategoryView(ListView):
    model = Post
    template_name = 'news/category.html'
    context_object_name = 'news'
    #queryset = Post.objects.all().order_by('-postCreated')
    #ordering = ['-postCreated']
    paginate_by = 6

    def get_queryset(self):
        self.id = self.kwargs.get('pk')
        cat = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(postCats=cat)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.id = self.kwargs.get('pk')
        cat = Category.objects.get(id=self.id)
        user = self.request.user
        if user.is_authenticated:
            is_subscribed = cat.subscribers.filter(email=user.email).exists()
            context['is_subscribed'] = is_subscribed
            context['category'] = cat
        else:
            context['category'] = cat
            redirect('/accounts/login/')
        return context

# Подписка на категорию
def subscribe_to_category(request, pk):
    category = Category.objects.get(id=pk)
    user = request.user
    if user.is_authenticated:
        category.subscribers.add(user)
    else:
        redirect('/accounts/login/')
    return redirect('news:category', pk=kwargs['pk'])

# Отписка от категории
def unsubscribe_from_category(request, pk):
    category = Category.objects.get(id=pk)
    user = request.user
    if user.is_authenticated:
        category.subscribers.remove(user)
    else:
        redirect('/accounts/login/')
    return redirect('news:category', pk=kwargs['pk'])


class SubscribeView(LoginRequiredMixin, TemplateView):
    template_name = 'news/subscribe.html'

    def post(self, request, *args, **kwargs):
        category_id = kwargs['pk'] # Извлекаем идентификатор категории из kwargs
        category = Category.objects.get(id=category_id)
        user = request.user
        if user.is_authenticated:
            category.subscribers.add(user)
        else:
            pass
        return redirect('news:category', pk=category_id)


class UnsubscribeView(LoginRequiredMixin, TemplateView):
    template_name = 'news/unsubscribe.html'

    def post(self, request, *args, **kwargs):
        category_id = kwargs['pk']
        category = Category.objects.get(id=category_id)
        user = request.user
        if user.is_authenticated:
            category.subscribers.remove(user)
        else:
            pass
        return redirect('news:category', pk=category_id)


def CategoryDetailView(request, pk):
   category = Category.objects.get(pk=pk)
   is_subscribed = True if len(category.subscribers.filter(id=request.user.id)) else False

   return render(request,'news/category.html',
                 {'postCats': category.id,
                  'is_subscribed' : is_subscribed,
                  'subscribers': category.subscribers.all()
                  })

# Получение списка подписчиков
def get_subscribers(category):
    user_email =[]
    user_name =[]
    for user in category.subscribers.all():
        user_email.append(user.email)
        user_name.append(user.username)
    return list(user_email), list(user_name)

# Отправка письма о новом посте
def new_post_subscriptions(instance):
    template = 'mail/new_post.html'

    for category in instance.postCats.all():
        email_subject = f'Новый пост в категории "{category}"'
        user_emails, user_names = get_subscribers(category)
        for user_email, user_name in zip(user_emails, user_names):
            html = render_to_string(
                    template_name=template,
                    context={
                      'category': category,
                        'post': instance,
                        'username': user_name,
                    }
                )
            msg = EmailMultiAlternatives(
                subject=f'Новый пост от [newspaper.com]. Тема: {instance.postTitle}',
                # это то же, что и message
                body=f'Привет, {user_name}. \n' \
                     f'{instance.postTitle} \n' \
                     f'{instance.postText}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user_email] # Обернем адрес электронной почты в список
            )
            msg.attach_alternative(html, 'text/html')
            msg.send()
