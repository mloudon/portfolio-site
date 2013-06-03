from mezzanine.conf import settings
from django.conf.urls import patterns, include, url

# Leading and trailing slahes for urlpatterns based on setup.
_slashes = (
    "/" if settings.BLOG_SLUG else "",
    "/" if settings.APPEND_SLASH else "",
)


# Custom patterns.
urlpatterns = patterns("portfolioapp.views",
    url("^%s(?P<slug>.*)%s$" % _slashes, "blog_post_detail",
        name="blog_post_detail"),
)