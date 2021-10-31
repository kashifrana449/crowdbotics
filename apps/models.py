from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class App(models.Model):
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=512)

    class Meta:
        db_table = 'app'

    def __str__(self):
        return self.name

    def get_subscriptions(self):
        return Subscription.objects.filter(app=self.id).all()


class Plan(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)
    price = models.IntegerField(default=0, null=False, blank=False)

    class Meta:
        db_table = 'plan'

    def __str__(self):
        return self.name


class Subscription(models.Model):
    plan = models.ForeignKey(Plan, related_name='plan_subscription', on_delete=models.CASCADE, null=False, blank=False)
    app = models.ForeignKey(App, related_name='app_subscription', on_delete=models.CASCADE, null=False, blank=False)
    created_date = models.DateTimeField(default=datetime.now, null=False, blank=False)
    status = models.BooleanField(default=True, null=False, blank=False)
