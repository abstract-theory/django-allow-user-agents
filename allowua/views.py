from django.views.generic import TemplateView
from django.http import HttpResponse

# Below is a list of bots that you might consider either allowing or
# blocking.
#
# Some common are listed bots is given below. The list is current as of
# April 2020.
#
# 'google', # Very well known search engine
# 'bing', # As of Oct. 2018, Bing is reported to have %36 of US market share
# 'baidu', # Chinese search engine
# 'duckduckgo', # American search engine
# 'yandex', # Russian search engine
# 'seznam', # Czech search engine
# 'applebot', # "Products like Siri and Spotlight Suggestions use Applebot"
# 'yahoo', # I haven't seen Yahoo or Slurp in logs lately
# 'msnbot', # MS is reported to still use this sometimes
# 'naver', # Korean search engine
# 'daum', # Korean search engine
# 'qwant', # American search engine
# 'exabot', # French search engine
# 'qihoo', # Chinese search engine
# 'soso', # Chinese search engine
# 'sogou', # Chinese search engine
# 'ia_archiver', # Alexa's crawlers, used for analytics


def check_agents(request, ua):
    user_agent = request.META.get('HTTP_USER_AGENT').lower()
    isWhiteListed = False
    for s in map(str.lower, ua):
        if s in user_agent:
            isWhiteListed = True
            break
    return isWhiteListed


def restrict_user_agents(user_agent_ids=()):
    def real_decorator(viewFunc):
        def wrapper(request, *args, **kwargs):
            if check_agents(request, user_agent_ids):
                result = viewFunc(request, *args, **kwargs)
            else:
                result = HttpResponse(status=404)
            return result
        return wrapper
    return real_decorator


class RestrictUserAgentsView(TemplateView):
    '''
    Note: the "get" function also handles HEAD requests
    '''

    user_agent_ids = []

    def __init__(self, *args, user_agent_ids=(), **kwargs):
        self.user_agent_ids = user_agent_ids
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if check_agents(request, self.user_agent_ids):
            return super().get(self, request, *args, **kwargs)
        else:
            return HttpResponse(status=404)


class TagUserAgentsView(TemplateView):
    '''
    Note: the "get" function also handles HEAD requests
    '''

    user_agent_ids = ()

    def __init__(self, *args, user_agent_ids=(), **kwargs):
        self.user_agent_ids = user_agent_ids
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        isWl = check_agents(request, self.user_agent_ids)
        return super().get(self, request, *args, user_agent_tagged=isWl, **kwargs)

