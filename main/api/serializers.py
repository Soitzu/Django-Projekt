from rest_framework import serializers
from inventory.models import Device
from app.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
