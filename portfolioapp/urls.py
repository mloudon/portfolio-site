from mezzanine.conf import settings
from django.conf.urls import patterns, url

# Leading and trailing slahes for urlpatterns based on setup.
_slashes = (
    "/" if settings.BLOG_SLUG else "",
    "/" if settings.APPEND_SLASH else "",
)


# Custom patterns.
urlpatterns = patterns("portfolioapp.views",
    (r"^%s(?P<slug>.*)%s$" % (_slashes), "blog_post_detail"),
)