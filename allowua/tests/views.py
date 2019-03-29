from django.http import HttpResponse
from ..views import AllowUA

USER_AGENTS = ['google', 'bing', 'baidu', 'duckduckgo', 'yandex', 'seznam', 'applebot',]

@AllowUA(user_agents = USER_AGENTS)
def test_view_function(request):
    return HttpResponse(status=200)    

