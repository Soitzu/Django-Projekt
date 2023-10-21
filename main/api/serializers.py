from rest_framework import serializers
from inventory.models import Device


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
