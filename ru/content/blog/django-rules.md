Title: О пермишенах в Django
Date: 2018-03-17T14:08:00
Tags: python, django
Slug: django-rules
Feed: true

<small>Дисклеймер: этот пост не про встроенную в Django систему пермишенов (модель `auth.Permission`), она ущербная и предназначена только для управления админкой.</small>

Один из вопросов, которые я всегда задаю на собеседовании, посвящён управлению пермишенами в Django. Я не спрашиваю об этом напрямую, а даю задачу, в которой надо использовать пермишены, и смотрю, как человек справляется. Вот эта задача:

> Сделать движок для коллективного ведения блога. Залогиненный пользователь может добавлять записи в блог. Редактировать или удалить запись может её автор или суперюзер.

Решение кандидата, обычно, выглядит примерно так:

```python
class AddPostView(...):

    def dispatch(self, request, *args, **kwargs):
        if not request.is_authenticated():
            return django.http.HttpResponseForbidden()
        return super(...)

class EditPostView(...):

    def dispatch(self, request, *args, **kwargs):
        ...
        if not (
            request.user.is_authenticated() or
            request.user.is_superuser or
            request.user == self.object.author
        ):
            return django.http.HttpResponseForbidden()
        return super(...)
```

Возможны также варианты с использованием `LoginRequiredMixin` или декоратора `login_required`, но сути дела это не меняет.

Ещё надо проверить пермишены в шаблоне, чтобы определить, надо ли показывать кнопку для редактирования записи:

```djangotemplate
{% if request.user.is_authenticated or request.user.is_superuser or request.user == post.author %}
  <a href="...">Edit</a>
{% endif %}
```

Допустим, что мы захотели добавить новую фичу: в первый день каждого месяца дать возможность всем пользователям (даже анонимным) редактировать любую запись в блоге. Для этого надо просто добавить одну строку во вьюху, так?

```python
if not (
    datetime.date.today().day == 1 or
    request.user.is_authenticated() or
    request.user.is_superuser or
    request.user == self.object.author
):
    ...
```

Добавили, всё классно. А потом приходит багрепорт, что кнопка редактирования не отображается в первый день месяца как положено, потому что мы забыли обновить шаблон.

Этот пример показывает существенный изъян такого подхода: у нас есть один и тот же набор правил, который надо поддерживать актуальным как минимум в двух местах. А если эти правила будут более сложными, то реализовать их в шаблонах может быть просто невозможно.

Решение у этой проблемы очень простое: проверка пермишенов должна быть выделана в отдельный компонент, к которому другие компоненты будут обращаться по мере необходимости.

Специально для этого есть отличная библиотека [rules](https://github.com/dfunckt/django-rules).

Перепишем наш пример с использованием этой библиотеки. Сначала надо задекларировать наш набор правил:

```python
# apps/blog/rules.py
from __future__ import absolute_import
import rules
import datetime

@rules.predicate
def is_first_day_in_month():
    return datetime.date.today().day == 1

@rules.predicate
def is_author(user, obj):
    return obj.author == user

rules.add_perm("blog.add_post", rules.is_authenticated)
rules.add_perm("blog.edit_post", is_first_day_in_month | rules.is_superuser | is_author)
```

потом подправить вьюхи:

```python
# apps/blog/views.py
from rules.contrib.views import PermissionRequiredMixin


class AddPostView(PermissionRequiredMixin, ...):

    permission_required = "blog.add_post"


class AddPostView(PermissionRequiredMixin, ...):

    permission_required = "blog.edit_post"

```

и шаблон:

```djangotemplate
{% load rules %}
{% has_perm "blog.edit_post" request.user post as can_edit %}
{% if can_edit %}
  <a href="...">Edit</a>
{% endif %}
```

Чтобы всё это заработало, надо добавить `rules` в `INSTALLED_APPS` и `rules.permissions.ObjectPermissionBackend` в `AUTHENTICATION_BACKENDS`.

В заключение хочу добавить, что в моём текущем проекте мы не используем именованные пермишены типа `blog.edit_post`. Вместо этого мы определяем ещё один предикат:

```python
can_edit_post = is_first_day_in_month | rules.is_superuser | is_author
```

и напрямую вызываем его там, где надо проверить пермишен:

```python
if can_edit_post(user, post):
    ...
```
