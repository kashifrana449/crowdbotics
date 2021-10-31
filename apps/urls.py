from django.conf.urls import include, url
from rest_framework import routers

from apps.views import AppViewSet, PlanViewSet, SubscriptionViewSet

router = routers.DefaultRouter()
router.register('app', AppViewSet, 'apps')
router.register('plan', PlanViewSet, 'plans')
router.register('subscription', SubscriptionViewSet, 'subscriptions')

urlpatterns = [
   url(r'^', include(router.urls)),
]