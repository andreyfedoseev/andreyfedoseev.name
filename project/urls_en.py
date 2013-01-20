from urls import *


urlpatterns = common_patterns + patterns('',
    url(r"^en/", include("project.local_urls")),
)
