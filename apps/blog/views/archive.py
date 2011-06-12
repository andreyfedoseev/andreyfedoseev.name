
def by_type(request):
    site = Site.objects.get_current()
    blog = get_object_or_404(Blog, site=site)
    types = []
    for type, name in ENTRY_TYPES:
        number = blog.published_entries().filter(entry_type=type).count()
        if number == 0:
            continue
        types.append({'type': type,
                      'title': _(u"%s entries" % type),
                      'number': number,
                      })

    return render_to_response("blog/by_type.html",
                              {'blog': blog, 'types': types},
                              context_instance=RequestContext(request))


def index_by_type(request, entry_type=None, page=None):
    if not entry_type:
        raise Http404()
    site = Site.objects.get_current()
    blog = get_object_or_404(Blog, site=site)
    entries = blog.published_entries().filter(entry_type=entry_type)
    if not entries.count():
        raise Http404()

    data = {
        'blog': blog,
        'entry_type': _("%s entries" % entry_type),
        'fixed_sidebar': True,
        'display_type': display_type(request)
    }
    data.update(paginate(entries, "blog:index_by_type",
                         kwargs={'entry_type': entry_type}, page=page))
    return render_to_response("blog/index.html", data,
                              context_instance=RequestContext(request))



def by_date(request):
    site = Site.objects.get_current()
    blog = get_object_or_404(Blog, site=site)
    data = {}
    month_titles = {}
    for entry in blog.published_entries():
        year = entry.publication_timestamp.year
        month = entry.publication_timestamp.month
        if year not in data:
            data[year] = {}
        if month not in data[year]:
            data[year][month] = 0
        if month not in month_titles:
            month_titles[month] = _(entry.publication_timestamp.strftime("%B"))
        data[year][month] = data[year][month] + 1

    years = []
    for year in sorted(data):
        y_data = {'value': year, 'months': []}
        for month in sorted(data[year].keys()):
            m_data = {'value': month, 'title': month_titles[month], 'number': data[year][month]}
            y_data['months'].append(m_data)
        years.append(y_data)

    return render_to_response("blog/by_date.html",
                              {'blog': blog, 'years': years},
                              context_instance=RequestContext(request))


def index_by_date(request, year=None, month=None, page=None):
    if not year:
        raise Http404()

    try:
        year = int(year)
    except ValueError:
        raise Http404()

    if month:
        try:
            month = int(month)
        except ValueError:
            raise Http404()
        if month < 1 or month > 12:
            raise Http404()

    site = Site.objects.get_current()
    blog = get_object_or_404(Blog, site=site)
    if month:
        entries = blog.published_entries().filter(publication_timestamp__year=year, publication_timestamp__month=month)
    else:
        entries = blog.published_entries().filter(publication_timestamp__year=year)

    if not entries.count():
        raise Http404()

    data = {
        'blog': blog,
        'year': year,
        'fixed_sidebar': True,
        'display_type': display_type(request)
    }
    if month:
        data['month'] = month
        data['month_title'] = _(datetime.date.today().replace(month=month).strftime("%B"))
    kwargs = {'year': year}
    if month:
        kwargs['month'] = month
    data.update(paginate(entries, "blog:index_by_date",
                         kwargs=kwargs, page=page))
    return render_to_response("blog/index.html", data,
                              context_instance=RequestContext(request))


def by_tag(request):
    site = Site.objects.get_current()
    blog = get_object_or_404(Blog, site=site)
    tags = list(Tag.objects.usage_for_queryset(blog.published_entries(), counts=True))
    tags.sort(key=lambda x: x.count, reverse=True)
    return render_to_response("blog/by_tag.html",
                              {'blog': blog, 'tags': tags},
                              context_instance=RequestContext(request))


def index_by_tag(request, tag=None, page=None):
    if not tag:
        raise Http404()
    try:
        tag = Tag.objects.get(name=tag)
    except Tag.DoesNotExist:
        raise Http404()
    site = Site.objects.get_current()
    blog = get_object_or_404(Blog, site=site)
    entries = TaggedItem.objects.get_by_model(blog.published_entries(), tag)
    if not entries.count():
        raise Http404()

    data = {
        'blog': blog,
        'tag': tag,
        'fixed_sidebar': True,
        'display_type': display_type(request)
    }
    data.update(paginate(entries, "blog:index_by_tag",
                         kwargs={'tag': tag}, page=page))
    return render_to_response("blog/index.html", data,
                              context_instance=RequestContext(request))



