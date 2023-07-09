from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .decorators import error_handler
from django.utils import timezone
from django.shortcuts import get_object_or_404

class BaseMethods(APIView):
  def __init__(self, serializer, model, **kwargs):
    super().__init__(**kwargs)
    self.ViewSerializer = serializer
    self.model = model

  @error_handler
  def post(self, request):
    request.data.update({
      'created_at': timezone.now(),
      'updated_at': timezone.now(),
    })
    serializer = self.ViewSerializer(data=request.data, context={ 'request': request })
    if serializer.is_valid():
      serializer.save()
      return Response({ 'process': 'Done!' }, status=status.HTTP_201_CREATED)
    else:
      return Response({ 'error': serializer.errors }, status=status.HTTP_409_CONFLICT)

  @error_handler
  def get(self, request, _id):
    if _id:
      obj = get_object_or_404(self.model, id=_id)
      dic = obj.__dict__
      del dic['_state']
      return Response({'result': dic}, status=status.HTTP_302_FOUND)
    else:
      obj = self.model.objects.all()
      for item in obj:
        dic = obj.__dict__
      del dic['_state']
      return Response({'result': dic}, status=status.HTTP_302_FOUND)
        
  
  @error_handler
  def put(self, request, _id):
    request.data.update({
      'updated_at': timezone.now()
    })
    data = request.data
    if 'password' in data.keys():
      del data['password']
    
    instance = get_object_or_404(self.model, id = _id)
    serializer = self.ViewSerializer(instance, data=data, context={ 'request': request }, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.update(instance, data)
    return Response({'result': serializer.validated_data }, status=status.HTTP_200_OK)

  @error_handler
  def delete(self, request, _id):
    self.model.objects.filter(id=_id).delete()
    return Response({'result': 'Done!' }, status=status.HTTP_200_OK)