=================
Allow User-Agents
=================

Overview
------------------------
**Allow User-Agents** is a Django app that alters the behavior of both view functions and template rendering in a manner that depends on the user-agent string. The intended purpose is to reduce nuisance bot traffic while remaining crawlable by search engines. To use with view functions, a decorator **@restrict_user_agents** is used. To use with templates directly from **urls.py**, the functions, **RestrictUserAgentsView.as_view(...)** and **TagUserAgentsView.as_view(...)** are used. Both **@restrict_user_agents** and **RestrictUserAgentsView.as_view(...)** return a **404** status code for non-white-listed user-agents. The other method, **TagUserAgentsView.as_view(...)**, passes a **boolean** value to the Django template for conditional rendering.


Requirements
------------------------
The included tests have been successfully run on the following Django versions: 1.9, 2.0, 3.0, 3.2


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
This decorator will cause a status code of **404** to be returned to clients if they do not have a white-listed user-agent. To use the decorator, create a list of sub-strings for user-agents you wish to allow. Then place the decorator above your view functions as shown below. The sub-strings are used to identify user-agents, and they are case-insensitive.

.. code-block:: python

    from allowua.views import restrict_user_agents

    # strings to identify user-agents
    UA = ('google', 'bing', 'baidu', 'duckduckgo', 'yandex',)

    @restrict_user_agents(user_agent_ids=UA)
    def view(request):
        # do something


RestrictUserAgentsView.as_view(...)
------------------------------------
This function returns **404** status code to clients if they do not have a white-listed user-agent.  It is called directly on templates in a manner similar to **TemplateView.as_view(...)**. In fact, this method is an over-ridden version of **TemplateView.as_view(...)**. Example syntax is shown below.

.. code-block:: python

    from allowua.views import RestrictUserAgentsView

    # strings to identify user-agents
    UA = ('google', 'bing', 'baidu', 'duckduckgo', 'yandex',)

    urlpatterns = [
        re_path(r'^hello-world/$', RestrictUserAgentsView.as_view(template_name='hello-world.html', user_agent_ids=UA)),
    ]


TagUserAgentsView.as_view(...)
----------------------------------
This function passes a value **True** to Django templates if a  white-listed user-agent was detected. Otherwise, it is **False**. The variable, **user_agent_tagged**, can then be used for conditional rendering in the template.  The function is called directly on templates in a manner similar to **TemplateView.as_view(...)**. In fact, this method is an over-ridden version of **TemplateView.as_view(...)**. Example syntax is shown below.

.. code-block:: python

    # urls.py
    from allowua.views import TagUserAgentsView

    UA = ('google', 'bing', 'baidu', 'duckduckgo', 'yandex',)

    urlpatterns = [
        re_path(r'^hello-world/$', TagUserAgentsView.as_view(template_name='hello-world.html', user_agent_ids=UA)),
    ]

In your Django templates, add an **{% if user_agent_tagged %}** statement that surrounds page elements. These elements will only be transmitted to clients who have white-listed user-agents.

.. code-block:: html

    <!-- template.html -->
    <html>
        <body>
            {%  if user_agent_tagged %}
                <p>Contrary to widespread rumors, as of August, 2021, no major search crawler fully renders JavaScript!</p>
            {%  else %}
                <script src="/bundle.js"></script>
            {%  endif %}
        </body>
    </html>



Testing
-------------------
To run the built-in dev tests using Django's test framework, run

.. code-block:: bash

    python3 manage.py test allowua

To further convince yourself that either **restrict_user_agents** or  **RestrictUserAgentsView.as_view(...)** is working with your particular project, try the below CURL commands on your protected pages. The first line should show "**404 Not Found**", while the second should show "**200 OK**".

.. code-block:: bash

    url='https://localhost/my/protected/page/'
    curl $url -kIS -H 'User-Agent: Mozilla/5.0'
    curl $url -kIS -H 'User-Agent: Googlebot'

To verify that **TagUserAgentsView.as_view(...)** is working with your particular project, try the below command instead.

.. code-block:: bash

    url='https://localhost/my/protected/page/'
    curl $url -kSs -H 'User-Agent: Mozilla/5.0' | grep HIDDEN_TEXT_STRING
    curl $url -kSs -H 'User-Agent: Googlebot' | grep HIDDEN_TEXT_STRING


