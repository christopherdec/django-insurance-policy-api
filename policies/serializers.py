from rest_framework import serializers

from .models import Policy


class PolicySerializer(serializers.ModelSerializer):
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Policy
        fields = '__all__'
