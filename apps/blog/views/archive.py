from blog.views import BlogViewMixin
from django.http import Http404
from django.utils.dateformat import format
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView


class Archive(BlogViewMixin, TemplateView):

    template_name = "blog/archive.html"

    def get_context_data(self, **kwargs):
        data = super(Archive, self).get_context_data(**kwargs)

        years = sorted(set(dt.year for dt in self.blog.published_entries().values_list("publication_timestamp", flat=True)), reverse=True)
        if not years:
            raise Http404()

        current_year = int(kwargs.get("year") or years[0])
        if current_year not in years:
            raise Http404()

        entries = self.blog.published_entries().filter(publication_timestamp__year=current_year).order_by("publication_timestamp")

        months = {}
        for entry in entries:
            month = entry.publication_timestamp.month
            if month in months:
                months[month]["entries"].append(entry)
            else:
                months[month] = dict(entries=[entry],
                                     name=format(entry.publication_timestamp, "F"))

        months = [r[1] for r in sorted(months.items())]

        page_title = _("Archive for %(year)i") % dict(year=current_year)

        data.update(dict(current_year=current_year,
                         years=years,
                         months=months,
                         page_title=page_title))

        return data
