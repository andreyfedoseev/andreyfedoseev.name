Title: Подстветка синтаксиса в Django
Date: 2010-03-04T07:54:00
Tags: django, веб-разработка
Slug: 24/podstvetka-sintaksisa-v-django
Feed: false

<p>Приделал к бложику подсветку синтаксиса. Для этого изобрел специальный template-тег для Django. В отличие от большинства существующих решений, подсветка делается не на стороне клиента, а на сервере. Ниже представлен исходный код, который вы можете свободно использовать.</p>
<!-- more -->
<p>Для работы этого тега требуется установленная утилита <a href="http://www.andre-simon.de/doku/highlight/en/highlight.html">highlight</a>. В Убунте она имеется, и, я думаю, что в других дистрибутивах тоже.</p>
<p>Код тега прост до безобразия:</p>

```python
from django import template
import subprocess, shlex


register = template.Library()


class HightlightNode(template.Node):

    def __init__(self, nodelist, format):
        self.nodelist = nodelist
        self.format = format

    def render(self, context):
        output = self.nodelist.render(context)
        args = shlex.split("highlight -S %s -f" % str(self.format))
        try:
            p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out, errors = p.communicate(output.encode('utf-8'))
            if out:
                output = out.decode('utf-8')
        except:
            pass

        return output


@register.tag(name="highlight")
def do_highlight(parser, token):
    parts = token.split_contents()
    tag_name = parts[0]
    args = parts[1:]
    if len(args) != 1:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % tag_name
    nodelist = parser.parse(('endhighlight',))
    parser.delete_first_token()
    return HightlightNode(nodelist, args[0])
```

<p>В шаблон это хозяйство вставляется следующим образом:</p>

    {% highlight py %}SOME PYTHON CODE{% endhighlight %}

<p>Параметр тега — это формат исходного кода. В данном случае это <em>py</em>, то есть Питон.</p>
<p>Кроме того, понадобится таблица стилей, чтобы полученный код заиграл новыми красками. Я, например, использую такую:</p>

```css
.hl.num {
  color: #2928ff;
}

.hl.esc {
  color: #ff00ff;
}

.hl.str {
  color: #ff0000;
}

.hl.dstr {
  color: #818100;
}

.hl.slc {
  color: #838183;
  font-style: italic;
}

.hl.com {
  color: #838183;
  font-style: italic;
}

.hl.dir {
  color: #008200;
}

.hl.sym {
  color: #000000;
}

.hl.line {
  color: #555555;
}

.hl.mark {
  background-color: #ffffbb;
}

.hl.kwa {
  color: #000000;
  font-weight: bold;
}

.hl.kwb {
  color: #830000;
}

.hl.kwc {
  color: #000000;
  font-weight: bold;
}

.hl.kwd {
  color: #010181;
}
```

<p>Пользуйтесь на здоровье.</p>
