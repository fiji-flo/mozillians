import mock

from django.test import RequestFactory
from django.test.utils import override_settings

from mozillians.common.tests import TestCase
from mozillians.dino_park import views
from mozillians.users.tests import UserFactory


class TestAPIEndpoints(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('mozillians.dino_park.views.requests.get')
    @mock.patch('mozillians.dino_park.views.UserAccessLevel')
    @override_settings(DINO_PARK_ORGCHART_SVC='orgchart-svc')
    def test_orgchart_allowed_as_staff(self, mock_scope, mock_get):
        response = mock.Mock()
        response.json.return_value = {'foo': 'bar'}

        # Mock UserAccessLevel class and attributes
        mock_scope.get_privacy.return_value = 'staff'
        mock_scope.STAFF = 'staff'

        mock_get.return_value = response
        request = self.factory.get('/')
        request.user = UserFactory.create()
        resp = views.orgchart(request)
        mock_get.assert_called_with('http://orgchart-svc/orgchart')
        self.assertEqual(resp.content, '{"foo": "bar"}')

    @mock.patch('mozillians.dino_park.views.requests.get')
    @mock.patch('mozillians.dino_park.views.UserAccessLevel')
    @override_settings(DINO_PARK_ORGCHART_SVC='orgchart-svc')
    def test_orgchart_allowed_as_private(self, mock_scope, mock_get):
        response = mock.Mock()
        response.json.return_value = {'foo': 'bar'}

        # Mock UserAccessLevel class and attributes
        mock_scope.get_privacy.return_value = 'private'
        mock_scope.PRIVATE = 'private'

        mock_get.return_value = response
        request = self.factory.get('/')
        request.user = UserFactory.create()
        resp = views.orgchart(request)
        mock_get.assert_called_with('http://orgchart-svc/orgchart')
        self.assertEqual(resp.content, '{"foo": "bar"}')

    @mock.patch('mozillians.dino_park.views.UserAccessLevel')
    @override_settings(DINO_PARK_ORGCHART_SVC='orgchart-svc')
    def test_orgchart_forbidden(self, mock_scope):
        mock_scope.get_privacy.return_value = 'dummy'
        request = self.factory.get('/')
        request.user = UserFactory.create()
        resp = views.orgchart(request)
        self.assertEqual(resp.status_code, 403)

    @mock.patch('mozillians.dino_park.views.requests.get')
    @mock.patch('mozillians.dino_park.views.UserAccessLevel')
    @override_settings(DINO_PARK_ORGCHART_SVC='orgchart-svc')
    def test_orgchart_get_by_id(self, mock_scope, mock_get):
        mock_scope.get_privacy.return_value = 'staff'
        mock_scope.STAFF = 'staff'
        response = mock.Mock()
        response.json.return_value = {'foo': 'bar'}
        mock_get.return_value = response
        request = self.factory.get('/')
        request.user = UserFactory.create()
        resp = views.orgchart_get_by_id(request, 'related', 'asdf')
        mock_get.assert_called_with('http://orgchart-svc/orgchart/related/asdf')
        self.assertEqual(resp.content, '{"foo": "bar"}')

    @mock.patch('mozillians.dino_park.views.UserAccessLevel')
    @override_settings(DINO_PARK_ORGCHART_SVC='orgchart-svc')
    def test_orgchart_related_forbidden(self, mock_scope):
        mock_scope.get_privacy.return_value = 'dummy'
        request = self.factory.get('/')
        request.user = UserFactory.create()
        resp = views.orgchart_get_by_id(request, 'related', 'abc')
        self.assertEqual(resp.status_code, 403)

    @mock.patch('mozillians.dino_park.views.requests.get')
    @mock.patch('mozillians.dino_park.views.UserAccessLevel')
    @override_settings(DINO_PARK_SEARCH_SVC='search-svc')
    def test_search_simple(self, mock_scope, mock_get):
        mock_scope.get_privacy.return_value = 'dummy'
        response = mock.Mock()
        response.json.return_value = {'foo': 'bar'}
        mock_get.return_value = response
        request = self.factory.get('/')
        request.user = UserFactory.create()
        resp = views.search_simple(request, 'asdf')
        mock_get.assert_called_with('http://search-svc/search/simple/dummy/asdf')
        self.assertEqual(resp.content, '{"foo": "bar"}')

    @mock.patch('mozillians.dino_park.views.requests.get')
    @mock.patch('mozillians.dino_park.views.UserAccessLevel')
    @override_settings(DINO_PARK_SEARCH_SVC='search-svc')
    def test_search_get_profile(self, mock_scope, mock_get):
        mock_scope.get_privacy.return_value = 'dummy'
        response = mock.Mock()
        response.json.return_value = {'foo': 'bar'}
        mock_get.return_value = response
        request = self.factory.get('/')
        request.user = UserFactory.create()
        resp = views.search_get_profile(request, 'asdf')
        mock_get.assert_called_with('http://search-svc/search/get/dummy/asdf')
        self.assertEqual(resp.content, '{"foo": "bar"}')
