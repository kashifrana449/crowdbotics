from rest_framework import serializers

from apps.models import App, Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True, many=False)
    plan_id = serializers.IntegerField(write_only=True, allow_null=False)
    app_id = serializers.IntegerField(write_only=True, allow_null=False)

    class Meta:
        model = Subscription
        exclude = ('app', )

    @staticmethod
    def validate_plan_id(plan_id):
        if not Plan.objects.filter(id=plan_id).exists():
            raise serializers.ValidationError('No plan with id %d exists' % plan_id)
        return plan_id

    def validate_app_id(self, app_id):
        try:
            app = App.objects.get(id=app_id)
            if app.owner_id != self.context['request'].user.id and not self.context['request'].user.is_superruser:
                raise serializers.ValidationError('you do not have permission on this app')
        except App.DoesNotExist:
            raise serializers.ValidationError('app with id %d does not exist' % app_id)
        return app_id


class AppSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSerializer(source='get_subscriptions', many=True, read_only=True)
    owner_id = serializers.IntegerField(write_only=True, allow_null=False)

    class Meta:
        model = App
        fields = '__all__'
        read_only_fields = ('owner', )

    def validate_owner_id(self, owner_id):
        if ((owner_id != self.context['request'].user.id)
                and not self.context['request'].user.is_superuser):
            raise serializers.ValidationError('only user create apps for himself/herself')
        return owner_id
