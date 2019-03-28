from django.urls import re_path
from ..views import AllowUAView
from .test_views import test_view_function

USER_AGENT_SUBSTRINGS = ['google', 'bing', 'baidu', 'duckduckgo', 'yandex', 'seznam', 'applebot',]

urlpatterns = [
    re_path(r'^test_as_view/$', AllowUAView.as_view(template_name='test.html', user_agents = USER_AGENT_SUBSTRINGS)),
    re_path(r'^test_decorator/$', test_view_function),
]
    
