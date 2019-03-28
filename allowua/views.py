from django.views.generic import TemplateView
from django.http import HttpResponse

# Below is a list of bots that you might consider either allowing or
# blocking. By default, Bing and Google are the bots allowed.
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
# 'qwant', # American privacy search engine
# 'exabot', # French search engine
# 'qihoo', # Chinese search engine
# 'soso', # Chinese search engine
# 'sogou', # Chinese search engine
# 'alexa', # used for the Alexa rankings

USER_AGENT_SUBSTRINGS = ['google', 'bing',]


class AllowUA():

    def __init__(self, user_agents = USER_AGENT_SUBSTRINGS):            
        # list of key words for user agents that you might wish to either allow or block.
        self.user_agent_substrings = user_agents
                
    def is_client_whitelisted(self, request):        
        user_agent = request.META.get('HTTP_USER_AGENT').lower()        
        isWhiteListed = False
        for s in self.user_agent_substrings:
            if s in user_agent:
                isWhiteListed = True
                break                    
        return isWhiteListed

    def __call__(self, viewFunc):        
        def f(request, *args, **kwargs):                    
            if self.is_client_whitelisted(request):
                result = viewFunc(request, *args, **kwargs)
            else:
                result = HttpResponse(status=404)
            return result
        return f


class AllowUAView(TemplateView):    
    
    user_agents = []
    
    def __init__(self, *args, user_agents = USER_AGENT_SUBSTRINGS, **kwargs):    
        self.aua = AllowUA(user_agents)
        super().__init__(*args, **kwargs)


    # request methods supported by "as_view(...)":
    def get(self, request, *args, **kwargs):
        '''
        Note: the "get" function also handles HEAD requests
        '''
        if self.aua.is_client_whitelisted(request):            
            return super().get(self, request, *args, **kwargs)            
        else:            
            return HttpResponse(status=404)

    
