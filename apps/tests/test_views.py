from json import dumps

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.models import Plan, App
from apps.views import PlanViewSet, AppViewSet, SubscriptionViewSet

User = get_user_model()


class ApisViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        plans = [
            {
                'name': 'Free',
                'price': 0,
            },
            {
                'name': 'Standard',
                'price': 10,
            },
            {
                'name': 'Pro',
                'price': 25,
            }
        ]
        for plan_item in plans:
            Plan.objects.get_or_create(**plan_item)
        cls.super_user = User.objects.create(username='kashif1', is_superuser=True)
        cls.user = User.objects.create(username='kashif2')
        user_app = {"name": "app-for-non-super-user", "description": "this app is being created user",
                    "owner_id": cls.user.id}
        super_user_app = {"name": "app-for-super-user", "description": "this app is being created by non super user",
                          "owner_id": cls.super_user.id}
        App.objects.get_or_create(**user_app)
        App.objects.get_or_create(**super_user_app)
        cls.factory = APIRequestFactory()

    def test_plans_list_for_super_user(self):
        view = PlanViewSet.as_view({'get': 'list'})
        request = self.factory.get('/apps/plan/')
        force_authenticate(request, user=self.super_user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_plan_for_super_user(self):
        view = PlanViewSet.as_view({'get': 'retrieve'}, detail=True)
        request = self.factory.get('/apps/plan/')
        force_authenticate(request, user=self.super_user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_plans_list_for_user(self):
        view = PlanViewSet.as_view({'get': 'list'})
        request = self.factory.get('/apps/plan/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_plan_for_user(self):
        view = PlanViewSet.as_view({'get': 'retrieve'}, detail=True)
        request = self.factory.get('/apps/plan/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_app_creation_user(self):
        view = AppViewSet.as_view({'post': 'create'})
        data = dumps({"name": "app-for-non-super-user", "description": "this app is being created by non super user",
                      "owner_id": self.user.id})
        request = self.factory.post('/apps/app/', data, content_type='application/json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_app_creation_super_user(self):
        view = AppViewSet.as_view({'post': 'create'})
        data = dumps({"name": "app-for-non-super-user", "description": "this app is being created by non super user",
                      "owner_id": self.super_user.id})
        request = self.factory.post('/apps/app/', data, content_type='application/json')
        force_authenticate(request, user=self.super_user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_app_creation_user_for_super_user(self):
        view = AppViewSet.as_view({'post': 'create'})
        data = dumps({"name": "app-for-non-super-user", "description": "this app is being created by non super user",
                      "owner_id": self.super_user.id})
        request = self.factory.post('/apps/app/', data, content_type='application/json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_app_list_for_super_user(self):
        view = AppViewSet.as_view({'get': 'list'})
        request = self.factory.get('/apps/app/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_app_list_for_user(self):
        view = AppViewSet.as_view({'get': 'list'})
        request = self.factory.get('/apps/app/')
        force_authenticate(request, user=self.super_user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_subs_creation(self):
        view = SubscriptionViewSet.as_view({'post': 'create'})
        data = dumps({"app_id":1, 'plan_id': 2, "status": True})
        request = self.factory.post('/apps/subscription/', data, content_type='application/json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)



