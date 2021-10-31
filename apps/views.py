from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.models import App, Plan, Subscription
from apps.serializers import AppSerializer, PlanSerializer, SubscriptionSerializer


class AppViewSet(ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if not self.request.user.is_superuser:
            self.queryset = self.queryset.filter(owner=self.request.user)
        return self.queryset


class PlanViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated, )


class SubscriptionViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if not self.request.user.is_superuser:
            self.queryset = self.queryset.filter(app__owner=self.request.user)
        return self.queryset

