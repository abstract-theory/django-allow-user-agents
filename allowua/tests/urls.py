import django
if django.VERSION[0] >= 2:
    from django.urls import re_path as version_url_path
else:
    from django.conf.urls import url as version_url_path

from ..views import RestrictUserAgentsView, TagUserAgentsView
from .views import test_view_function

USER_AGENT_SUBSTRINGS = ('google', 'bing', 'baidu', 'duckduckgo', 'yandex', 'seznam', 'applebot',)

urlpatterns = [
    version_url_path(r'^test_allow_view/$', RestrictUserAgentsView.as_view(template_name='hello-world.html', user_agent_ids=USER_AGENT_SUBSTRINGS)),
    version_url_path(r'^test_dual_view/$', TagUserAgentsView.as_view(template_name='hello-world.html', user_agent_ids=USER_AGENT_SUBSTRINGS)),
    version_url_path(r'^test_decorator/$', test_view_function),
]
