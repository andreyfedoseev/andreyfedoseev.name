from blog.models import Blog, Entry, Comment
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.management import BaseCommand
from django.core.urlresolvers import resolve, Resolver404
from django.utils.html import strip_tags
from dateutil.parser import parse
import requests
import json
import urlparse


ACTIVITIES_FEED_URL = "https://www.googleapis.com/buzz/v1/activities/%(author_id)s/@public?alt=json&max-results=50&key=%(api_key)s"


class Command(BaseCommand):

    def handle(self, *args, **options):

        cnt = 0
        domain = Site.objects.get_current().domain
        api_key = getattr(settings, "GOOGLE_API_KEY", None)
        if not api_key:
            raise ImproperlyConfigured("Missing GOOGLE_API_KEY value.")

        for blog in Blog.objects.all():
            if not blog.author_google_buzz_id:
                continue

            if blog.language == settings.LANGUAGE_CODE:
                urlconf = settings.ROOT_URLCONF
            else:
                urlconf = "%s_%s" % (settings.ROOT_URLCONF, blog.language)

            activities_feed_url = ACTIVITIES_FEED_URL % dict(author_id=blog.author_google_buzz_id,
                                                             api_key=api_key)
            response = requests.get(activities_feed_url)

            if not response.ok:
                continue

            for activity in json.loads(response.content)["data"]["items"]:
                if activity["object"]["type"] != "note":
                    continue
                crosspost_source = activity.get("crosspostSource")
                if not crosspost_source:
                    continue
                parsed_url = urlparse.urlparse(crosspost_source)
                if parsed_url.netloc != domain:
                    continue
                try:
                    resolver = resolve(parsed_url.path, urlconf=urlconf)
                except Resolver404:
                    continue

                if resolver.url_name != "entry":
                    continue

                entry_id = int(resolver.kwargs["id"])
                try:
                    entry = Entry.objects.get(blog=blog, id=entry_id,
                                              published=True)
                except Entry.DoesNotExist:
                    continue


                if Comment.objects.exclude(google_buzz_id=None).filter(entry=entry).count() == activity["links"]["replies"][0]["count"]:
                    continue

                comments_url = activity["links"]["replies"][0]["href"] + "&key=" + api_key
                response = requests.get(comments_url)
                if not response.ok:
                    continue
                for comment in json.loads(response.content)["data"]["items"]:
                    comment_id = comment["id"]
                    if Comment.objects.filter(google_buzz_id=comment_id).exists():
                        continue
                    author_name = comment["actor"]["name"]
                    author_url = comment["actor"]["profileUrl"]
                    text = strip_tags(comment["content"].replace("<br />", "\n"))
                    by_author = comment["actor"]["id"] == blog.author_google_buzz_id
                    timestamp = parse(comment["published"])
                    Comment.objects.create(entry=entry, text=text,
                                           google_buzz_id=comment_id,
                                           author_name=author_name,
                                           author_url=author_url,
                                           by_blog_author=by_author,
                                           timestamp=timestamp)
                    cnt += 1
                    
        print "Fetched %i new comments." % cnt