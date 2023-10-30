# Skillfactory Module D. Theme D6

Completed homework for Skillfactory Course: 'Python Web Developer'. Module D - 'Backend-development in Python and Django'. Theme D6 - 'Working with Mail and Completing Scheduled Tasks in Django'.

## Репозиторий учебного проекта NewsPaper для курсов "Веб-разработчик на Python" и "Fullstack-разработчик на Python"
### [Модуль D. Тема D6 "Работа с почтой и выполнение задач по расписанию"](https://victorinca.github.io/Skillfactory-Module-D-Theme-D6/)

Приложение новостного портала NewsPaper, созданное с помощью Python и Django, чтобы можно было: 1) смотреть новости 2) читать статьи.

Итоговое задание по теме D6 "Работа с почтой и выполнение задач по расписанию" заключается в создании возможности подписки на категории, автоматической отправки писем и рассылок, установление периодических задач.

База данных: sqlite.

Состоит из приложений news и accounts.

#### Приложение news включает в себя модели:
1) Author - авторы статей, новостей (далее - постов).
2) Category - категории постов - темы, которые они отражают (бизнес и экономика, наука и технологии, образование и вакансии, стиль жизни и здоровье и т.д.).
3) Post - посты (статьи и новости), которые создают пользователи. Каждый объект может иметь одну или несколько категорий.
4) PostCategory - промежуточная модель (явная) для связи "многие ко многим".
5) Comment - хранение комментариев к постам, оставляемых под каждой новостью/статьёй.
6) Subscription - подписки на категории.

Все модели собраны в единый скрипт (код) в приложении news в файл models.py.

#### В качестве результата задания нужно усовершенствовать новостной портал NewsPaper.

1) В категории должна быть возможность пользователей подписываться на рассылку новых статей в этой категории.
Для добавления пользователю возможности подписываться на рассылку новостей в какой-либо категории:

1.1) Добавить поле subscribers (соотношение manytomany), в которое будут записываться пользователи, подписанные на обновления в данной категории.

1.2) На самом сайте должна быть возможность пользователю подписаться на категорию (добавить маленькую кнопку "Подписаться», когда пользователь находится на странице новостей в какой-то категории).

1.3) При создании новости в этой категории подписчикам этой категории на адреса их почтовых ящиков, указанные при регистрации, автоматически отправляется/ приходит сообщение о пополнении в разделе. 
Письмо с HTML-кодом заголовка и первыми 50 символами текста статьи.
В теме письма должен быть сам заголовок статьи. 

1.4) Текст состоит из вышеуказанного HTML и текста: "Здравствуй, username. Новая статья в твоём любимом разделе!".
Содержание письма остаётся на ваше усмотрение, главное, чтобы в нём была отражена краткая информация о данной новости.
В письме обязательно должна быть гиперссылка на саму статью, чтобы получатель мог по клику перейти и прочитать её.

2) Добавить приветственное письмо, которое отправляется пользователю при регистрации в приложении. Содержание и посыл письма остается на выбор, главное — обязательно добавить ссылку на активацию и указать в нём имя пользователя!

3) Если пользователь подписан на какую-либо категорию, то каждую неделю ему приходит на почту список новых статей, появившийся за неделю, с гиперссылками на статьи, чтобы пользователь мог перейти и прочесть любую из статей.

4) Установить лимит на публикации - один пользователь не может публиковать более трёх новостей в сутки.

5) Периодические задачи: добавить рассылку писем еженедельно с новыми статьями, добавленными за неделю в разделе, на который подписан пользователь.

#### Запуск проекта

1) Создать виртуальное окружение (далее - ВО) - изолированну версию Python, которая находится у вас в папке venv:

python -m venv venv

2) Активировать ВО:

2.1) В Windows _PowerShell_ или _cmd_:

venv\sripts\activate

2.2) В Windows _GitBash_

source venv/sripts/activate

2.3) Linux, MacOS

source venv/bin/activate

3) Установить через pip

3.1) Django с активированной средой (в виртуальную среду):

python -m pip install Django

3.2) Дополнительные пакеты:

pip install django-filter

pip install django-dbbackup

pip install django-allauth

pip install django-apscheduler

4) Перейти в папку проекта, где находится файл manage.py с помощью команды: cd название_папки, например, 

cd NewsPaper

5) Проверить, что находимся в нужной папке с помощью команды ls. Если после выполнения команды в терминале виден файл manage.py - можно запускать проект. Иначе - см. п.4. 

6) Запускаем проект командой 

python manage.py runserver

или

./manage.py runserver

Сообщение говорит нам о том, что приложение начало работу по адресу 127.0.0.1:8000.

Открываем любой браузер и переходим по адресу http://127.0.0.1:8000/.

Полезные команды:

- посмотреть список доступных команд для Django:

python manage.py help

#### Доступы в приложении - учётные записи

Панель администратора:
http://127.0.0.1:8000/admin/ 

Администратор:
- логин: admin
- пароль: admin-admin

Пользователи:
- логин: user1@mail.com
- пароль: user1-user1

- логин: user2@mail.com
- пароль: user2-user2

- логин: test1@mail.com
- пароль: test1-test1

и т.п.

- логин: test5@mail.com
- пароль: test5-test5

## Поддержать, отблагодарить автора
Если представленная работа Вам понравилась, принесла пользу, сэкономила время, то Вы можете поддержать автора, воспользовавшись различными платежными системами.
- [Поддержать автора через ЮMoney](https://yoomoney.ru/to/4100117804016773)
- [Выразить признательность через Qiwi](https://qiwi.com/n/VICTORINCA)
- [Поблагодарить автора через WebMoney](https://donate.webmoney.com/w/7MSQEs4xcygHPpeLcLATP)
#### Благодарю Вас за щедрость!
#### Ваша поддержка и признательность очень приятны и важны!

## Ссылки

- [Ссылка на страницу проекта](https://victorinca.github.io/Skillfactory-Module-D-Theme-D6/)
- [Ссылка на GitHub](https://github.com/Victorinca/Skillfactory-Module-D-Theme-D6)
  
По всем вопросам, которые касаются выполненного задания, можно писать на почту victoriavladimirskaya@gmail.com.