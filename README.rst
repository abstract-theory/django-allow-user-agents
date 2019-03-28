=================
Allow User-Agents
=================

Overview
------------------------
**Allow User-Agents** is a Django app that limits page access to whitelisted user-agents. The purpose is to reduce nuisance bot traffic while remaining crawlable by desirable bots such as search engines. The app can be called as a decorator on view functions. There is also an **as_view(...)** function that can be called from **urls.py**.


Requirements
------------------------
I've tested this on Django version 2.1. I expect it to run on earlier versions. There are some built-in dev tests, and they're designed to accommodate Django versions before 2.0.


Installation
------------------------
Drop the source folder into your Django project as you would any other Django app. You will need to add '**allowua.apps.AllowUserAgentsConfig**' to your settings file in the **INSTALLED_APPS** list in **settings.py**:

.. code-block:: python

    INSTALLED_APPS = [
        ...        
        'allowua.apps.AllowUserAgentsConfig',
    ]


Using the decorator 
-------------------

Use the decorator by creating a list of sub-strings for user-agents that you wish to allow. Then place the decorator above your view functions:

.. code-block:: python

    from allowua.views import AllowUA
    
    USER_AGENT_SUBSTRINGS = ['google', 'bing', 'baidu', 'duckduckgo', 'yandex',]    

    @AllowUA(user_agents = USER_AGENTS)
    def view(request):
        # do something

Using the as_view(...) function
-------------------------------    
It can also be called directly on templates in a manner similar to **TemplateView.as_view(...)**. In fact, this method is an over-ridden version of **TemplateView.as_view(...)**. Example syntax is shown below.

.. code-block:: python

    from allowua.views import AllowUAView
    
    USER_AGENT_SUBSTRINGS = ['google', 'bing', 'baidu', 'duckduckgo', 'yandex',]
    
    urlpatterns = [
        re_path(r'^hello-world/$', AllowUAView.as_view(template_name='hello-world.html', user_agents = USER_AGENT_SUBSTRINGS)),
    ]
    

Testing
-------------------
To convince yourself that it is working with your particular project, try the below CURL commands on your protected pages. The first line should show "**404 Not Found**", while the second should show "**200 OK**".

.. code-block:: bash

    url='https://localhost/my/protected/page/'    
    curl $url -kIS -H 'User-Agent: Mozilla/5.0'
    curl $url -kIS -H 'User-Agent: Googlebot'
    
To run the built-in dev tests using Django's test framework, run

.. code-block:: bash
    
    python3 manage.py test allowua
