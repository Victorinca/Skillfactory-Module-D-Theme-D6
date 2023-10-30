# Не забываем импортировать нужные функции и пакеты
from django.shortcuts import render, reverse, redirect
from django.utils import timezone
from datetime import datetime
from django.urls import reverse_lazy
#from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# импортируем необходимые дженерики
from django.views.generic import TemplateView
from django.views import View

# Create your views here.
class CabinetView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

# Добавляем функциональное представление для повышения привилегий пользователя до членства в группе authors
@login_required
def upgrade_me(request):
   user = request.user
   authors_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       authors_group.user_set.add(user)
   return redirect('/accounts/cabinet/')

