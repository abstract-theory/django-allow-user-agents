
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

import os

from ..views import check_agents
from .user_agents import user_agents_not_white_listed, white_listed_user_agents


TEST_TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.dirname(__file__), ],
    },
]

user_agents = ('google', 'bing', 'baidu', 'duckduckgo', 'yandex', 'seznam', 'applebot',)
rf = RequestFactory()


@override_settings(ROOT_URLCONF="allowua.tests.urls", TEMPLATES=TEST_TEMPLATES)
class AllowUserAgentsTests(TestCase):

    def test_function_whitelisted_clients(self):
        for user_agent in white_listed_user_agents:
            req = rf.get('/arbitrary-url/', HTTP_USER_AGENT=user_agent)
            res = check_agents(req, user_agents)
            self.assertEqual(res, True)

    def test_function_clients_not_whitelisted(self):
        for user_agent in user_agents_not_white_listed:
            req = rf.get('/arbitrary-url/', HTTP_USER_AGENT=user_agent)
            res = check_agents(req, user_agents)
            self.assertEqual(res, False)


    def test_decorator_whitelisted_clients(self):
        for user_agent in white_listed_user_agents:
            res = self.client.get('/test_decorator/', HTTP_USER_AGENT=user_agent)
            self.assertEqual(res.status_code, 200)

    def test_decorator_clients_not_whitelisted(self):
        for user_agent in user_agents_not_white_listed:
            res = self.client.get('/test_decorator/', HTTP_USER_AGENT=user_agent)
            self.assertEqual(res.status_code, 404)


    def test_AllowView_whitelisted(self):
        for user_agent in white_listed_user_agents:

            res = self.client.get('/test_allow_view/', HTTP_USER_AGENT=user_agent)
            self.assertEqual(res.status_code, 200)

            res = self.client.head('/test_allow_view/', HTTP_USER_AGENT=user_agent)
            self.assertEqual(res.status_code, 200)


    def test_AllowView_not_whitelisted(self):
        for user_agent in user_agents_not_white_listed:

            res = self.client.get('/test_allow_view/', HTTP_USER_AGENT=user_agent)
            self.assertEqual(res.status_code, 404)

            res = self.client.head('/test_allow_view/', HTTP_USER_AGENT=user_agent)
            self.assertEqual(res.status_code, 404)


    def test_DualView_whitelisted(self):
        for user_agent in white_listed_user_agents:

            res = self.client.get('/test_dual_view/', HTTP_USER_AGENT=user_agent)
            self.assertTrue(b'Hidden Text' in res.content)


    def test_DualView_not_whitelisted(self):
        for user_agent in user_agents_not_white_listed:

            res = self.client.get('/test_dual_view/', HTTP_USER_AGENT=user_agent)
            self.assertFalse(b'Hidden Text' in res.content)


