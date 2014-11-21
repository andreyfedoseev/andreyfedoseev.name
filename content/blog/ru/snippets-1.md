Title: Сниппеты #1
Date: 2011-09-23T08:45:00
Tags: django, python
Slug: 56
Feed: false

Время от времени буду выкладывать небольшие кусочки кода собственного сочинения. Буду рад, если кому-то они пригодятся. И ещё больше рад, если кто-то придумает, как их улучшить. Сегодня таких кусочков будет два.

**Номер раз**. Дано: Django и модель с несколькими текстовыми полями. Надо сделать простейший поиск по этим полям. При этом достаточно, чтобы искомый текст содержался хотя бы в одном поле.
И самое интересное — список полей для поиска заранее не определён, он может варьироваться.

    #!python
    from django.db import models

    class MyModel(models.Model):
    
        field_1 = models.CharField(max_length=100)
        field_2 = models.CharField(max_length=100)
        field_3 = models.CharField(max_length=100)
        
Поиск по одному полю сделать просто:

    #!python
    MyModel.objects.filter(field_1__icontains=search_term)

В случае с несколькими полями их нужно соединить оператором `OR`. В Django это делается так:

    #!python
    MyModel.objects.filter(
        models.Q(field_1__icontains=search_term) | models.Q(field_2__icontains=search_term)
    )
    
А что делать, если полей много и они заранее не известны? Например, названия полей хранятся в списке:

    #!python
    fields_to_search = ["field_1", "field_2", "field_3"]
    
Я сделал вот так:

    #!python
    from operators import or_
    
    MyModel.objects.filter(
        reduce(or_, map(
            lambda f: models.Q(**{f+"__icontains":search}),
            fields_to_search)
        ))
    )
    

**Номер два**. Надо узнать дату первого дня текущей недели. Например, сегодня пятница, 23 сентября 2011 года. В этом случае, какое число было в понедельник?

Я сделал вот так:

    #!python
    import datetime
    import calendar

    today = datetime.date.today()
    cal = calendar.Calendar()

    # Или, если неделя начинатеся с воскресенья
    # cal = calendar.Calendar(6)

    week_start_date = None  # Сюда мы сохраним искомую дату
    for week in cal.monthdatescalendar(today.year, today.month):
        if today in week:
            week_start_date = week[0]
            break

