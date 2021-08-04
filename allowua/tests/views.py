from django.http import HttpResponse
from ..views import restrict_user_agents

USER_AGENTS = ('google', 'bing', 'baidu', 'duckduckgo', 'yandex', 'seznam', 'applebot',)

@restrict_user_agents(user_agent_ids=USER_AGENTS)
def test_view_function(request):
    return HttpResponse(status=200)

