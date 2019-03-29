=================
Allow User-Agents
=================

Overview
------------------------
**Allow User-Agents** is a Django app that limits page access to whitelisted user-agents. The purpose is to reduce nuisance bot traffic while remaining crawlable by desirable bots such as search engines. The app can be called as a decorator on view functions. There are also two **as_view(...)** functions, **AllowUAView.as_view(...)** and **DualUAView.as_view(...)**. There are called from **urls.py**. The former returns a **404** status code, while the latter hides specific page content.


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


The view function decorator 
---------------------------
This decorator will cause a status code of **404** to be returned to clients if they do not have a white-listed user-agent. Use the decorator by creating a list of sub-strings for user-agents that you wish to allow. Then place the decorator above your view functions as shown below.

.. code-block:: python

    from allowua.views import allow_ua
    
    USER_AGENT_SUBSTRINGS = ['google', 'bing', 'baidu', 'duckduckgo', 'yandex',]    

    @allow_ua(user_agents = USER_AGENTS)
    def view(request):
        # do something


AllowUAView.as_view(...)
------------------------
This function returns **404** status code to clients if they do not have a white-listed user-agent.  It is called directly on templates in a manner similar to **TemplateView.as_view(...)**. In fact, this method is an over-ridden version of **TemplateView.as_view(...)**. Example syntax is shown below.

.. code-block:: python

    from allowua.views import AllowUAView
        
    UA = ['google', 'bing', 'baidu', 'duckduckgo', 'yandex',]
    
    urlpatterns = [
        re_path(r'^hello-world/$', AllowUAView.as_view(template_name='hello-world.html', user_agents=UA)),
    ]


DualUAView.as_view(...)
-----------------------
This function hide HTML page elements from clients if they do not have a white-listed user-agent.  It is called directly on templates in a manner similar to **TemplateView.as_view(...)**. In fact, this method is an over-ridden version of **TemplateView.as_view(...)**. Example syntax is shown below.

.. code-block:: python

    from allowua.views import DualUAView
        
    UA = ['google', 'bing', 'baidu', 'duckduckgo', 'yandex',]
    
    urlpatterns = [
        re_path(r'^hello-world/$', DualUAView.as_view(template_name='hello-world.html', user_agents=UA)),
    ]    

In your Django templates, add an **{% if show_hidden %}** statement that surrounds page elements. These elements will only be transmitted to clients who have white-listed user-agents.

.. code-block:: html

    <html>
        <body>        
            <h3>Hello World!</h3>
            {% if show_hidden %}
                <h3>Hidden Text</h3>        
            {% endif %}
        </body>
    </html>
    

Testing
-------------------
To convince yourself that either **allow_ua** or  **AllowUAView.as_view(...)** is working with your particular project, try the below CURL commands on your protected pages. The first line should show "**404 Not Found**", while the second should show "**200 OK**".

.. code-block:: bash

    url='https://localhost/my/protected/page/'    
    curl $url -kIS -H 'User-Agent: Mozilla/5.0'
    curl $url -kIS -H 'User-Agent: Googlebot'

To verify that **DualUAView.as_view(...)** is working with your particular project, try the below command instead.

.. code-block:: bash

    url='https://localhost/my/protected/page/'    
    curl $url -kSs -H 'User-Agent: Mozilla/5.0' | grep HIDDEN_TEXT_STRING
    curl $url -kSs -H 'User-Agent: Googlebot' | grep HIDDEN_TEXT_STRING
    
To run the built-in dev tests using Django's test framework, run

.. code-block:: bash
    
    python3 manage.py test allowua
