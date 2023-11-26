from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import Todo
from .serializers import *
from django.http import Http404


@api_view(['GET'])
def getTodo(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def addTodo(request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["DELETE"])
def deleteTodo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        raise Http404

    todo.delete()
    return Response(status=204)
