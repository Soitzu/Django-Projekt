from rest_framework.response import Response
from rest_framework.decorators import api_view
from inventory.models import Device
from .serializers import ItemSerializer


@api_view(['GET'])
def getData(request):
    devices = Device.objects.all()
    serializer = ItemSerializer(devices, many=True)
    return Response(serializer.data)
