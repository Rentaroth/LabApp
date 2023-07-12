import jwt
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UsersSerializer, GroupsSerializer, InvitationsSerializer, ExperimentsSerializer, SamplesSerializer, TestsSerializer, ResultsSerializer
from .models import Users, Groups, Invitations, Experiments, Samples, Tests, Results
from .decorators import error_handler, jwt_protection
from .base_methods import BaseMethods
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.conf import global_settings as settings
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from .docs import POST_METHOD_DOCS, GET_METHOD_DOCS, PUT_METHOD_DOCS, DELETE_METHOD_DOCS

class LoginView(APIView):
  @error_handler
  def post(self, request):
    credentials = request.data
    serializer = UsersSerializer(data=credentials, context={'request': request}, partial=True)
    if serializer.is_valid(raise_exception=True):
      try:
        user_obj = get_object_or_404(Users, username=credentials['username'])
        user = user_obj.__dict__
        if check_password(credentials['password'], user['password']):
          user = {i: j for i, j in user.items() if i in ['id', 'username', 'email']}
          user.update({
            'exp': datetime.utcnow()+timedelta(days=1)
          })
          token = jwt.encode(user, settings.SECRET_KEY,algorithm='HS256')
          return Response({'token': token}, status=status.HTTP_202_ACCEPTED)
        else:
          return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
      except Exception as err:
        print(str(err))
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
  @error_handler
  def post(self, request):
    try:
      refresh_token = request.data['refresh_token']
      token = RefreshToken(refresh_token)
      token.blacklist()
      return Response('Log out successfully')
    except Exception as err:
      return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=UsersSerializer, model=Users)

  @extend_schema(tags=['user'], request= UsersSerializer, **POST_METHOD_DOCS)
  @error_handler
  def post(self, request):
    request.data.update({
      'password': make_password(request.data['password']),
      'created_at': timezone.now(),
      'updated_at': timezone.now(),
    })
    serializer = self.ViewSerializer(data=request.data, context={ 'request': request })
    if serializer.is_valid():
      serializer.save()
      return Response({ 'process': 'Done!' }, status=status.HTTP_201_CREATED)
    else:
      return Response({ 'error': serializer.errors }, status=status.HTTP_409_CONFLICT)

  @extend_schema(tags=['user'], request=UsersSerializer, **GET_METHOD_DOCS)
  @error_handler
  def get(self, request, _id):
    obj = get_object_or_404(self.model, id=_id)
    dic = obj.__dict__
    del dic['password']
    del dic['_state']
    return Response({'result': dic}, status=status.HTTP_302_FOUND)

  @extend_schema(tags=['user'], request=UsersSerializer, **PUT_METHOD_DOCS)
  @error_handler
  def put(self, request, _id):
    return super().put(self, request, _id)

  @extend_schema(tags=['user'], request=UsersSerializer, **DELETE_METHOD_DOCS)
  @error_handler
  def delete(self, request, _id):
    return super().delete(self, request, _id)

class GroupsMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=GroupsSerializer, model=Groups)

  @extend_schema(tags=['groups'], request=GroupsSerializer, **POST_METHOD_DOCS)
  @error_handler
  def post(self, request):
    return super().post(self, request)


  @extend_schema(tags=['groups'], request=GroupsSerializer, **GET_METHOD_DOCS)
  @error_handler
  def get(self, request, _id):
    obj = get_object_or_404(self.model, id=_id)
    dic = obj.__dict__
    joins = obj.users_id.all()
    dic['members'] = []
    for item in joins:
      item_dic = item.__dict__
      print(item_dic)
      clean = {i: j for i, j in item_dic.items() if i not in ['_state', 'password']}
      dic['members'].append(clean)
    result = {i: j for i, j in dic.items() if i not in ['_state']}
    return Response({'result': result}, status=status.HTTP_302_FOUND)

  @extend_schema(tags=['groups'], request=GroupsSerializer, **PUT_METHOD_DOCS)
  @error_handler
  def put(self, request, _id):
    return super().put(self, request, _id)

  @extend_schema(tags=['groups'], request=GroupsSerializer, **DELETE_METHOD_DOCS)
  @error_handler
  def delete(self, request, _id):
    return super().delete(self, request, _id)

class JoiningGroups(APIView):
  serializer = GroupsSerializer
  model = Groups
  
  @extend_schema(tags=['accept_invitation'], request=GroupsSerializer, **PUT_METHOD_DOCS)
  @jwt_protection
  def put(self, request, inv_token):
    decoded = jwt.decode(inv_token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = decoded.get('_to')
    group_id = decoded.get('group_id')
    group = get_object_or_404(self.model, id=group_id)

    group.users_id.add(user_id)
    group.save()
    res = group.users_id.all()
    res_dic = []
    for item in res:
      dic = item.__dict__
      del dic['_state']
      del dic['password']
      res_dic.append(dic)
    
    return Response({ 'process': 'Done!', 'changes': [*res_dic] }, status=status.HTTP_200_OK)

class InvitationsMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=InvitationsSerializer, model=Invitations)

  @extend_schema(tags=['invitations'], request=InvitationsSerializer, **POST_METHOD_DOCS)
  @jwt_protection
  def post(self, request):
    _from = request.data['validated_token']
    print(_from)
    request.data.update({
      '_from': _from['id'],
      'created_at': timezone.now(),
      'updated_at': timezone.now(),
    })
    info = {i: j for i, j in request.data.items() if i not in ['created_at', 'updated_at', 'validated_token']}
    info.update({
      'exp': datetime.utcnow()+timedelta(days=1)
    })
    request.data['token'] = jwt.encode(info, settings.SECRET_KEY, algorithm='HS256')
    serializer = self.ViewSerializer(data=request.data, context={ 'request': request })
    if serializer.is_valid():
      serializer.save()
      return Response({ 'process': 'Done!' }, status=status.HTTP_201_CREATED)
    else:
      return Response({ 'error': serializer.errors }, status=status.HTTP_409_CONFLICT)

  @extend_schema(tags=['invitations'], request=InvitationsSerializer, **GET_METHOD_DOCS)
  @error_handler
  def get(self, request, _id):
    return super().get(self, request, _id)

  @extend_schema(tags=['invitations'], request=InvitationsSerializer, **PUT_METHOD_DOCS)
  @error_handler
  def put(self, request, _id):
    return super().put(self, request, _id)

  @extend_schema(tags=['invitations'], request=InvitationsSerializer, **DELETE_METHOD_DOCS)
  @error_handler
  def delete(self, request, _id):
    return super().delete(self, request, _id)

class ExperimentsMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=ExperimentsSerializer, model=Experiments)

  @extend_schema(tags=['experiments'], request=ExperimentsSerializer, **POST_METHOD_DOCS)
  @error_handler
  def post(self, request, _id):
    return super().post(self, request, _id)

  @extend_schema(tags=['experiments'], request=ExperimentsSerializer, **GET_METHOD_DOCS)
  @error_handler
  def get(self, request, _id):
    return super().get(self, request, _id)

  @extend_schema(tags=['experiments'], request=ExperimentsSerializer, **PUT_METHOD_DOCS)
  @error_handler
  def put(self, request, _id):
    return super().put(self, request, _id)

  @extend_schema(tags=['experiments'], request=ExperimentsSerializer, **DELETE_METHOD_DOCS)
  @error_handler
  def delete(self, request, _id):
    return super().delete(self, request, _id)

class SamplesMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=SamplesSerializer, model=Samples)
  
  @extend_schema(tags=['samples'], request=SamplesSerializer, **POST_METHOD_DOCS)
  @error_handler
  def post(self, request, _id):
    return super().post(self, request, _id)

  @extend_schema(tags=['samples'], request=SamplesSerializer, **GET_METHOD_DOCS)
  @error_handler
  def get(self, request, _id):
    return super().get(self, request, _id)

  @extend_schema(tags=['samples'], request=SamplesSerializer, **PUT_METHOD_DOCS)
  @error_handler
  def put(self, request, _id):
    return super().put(self, request, _id)

  @extend_schema(tags=['samples'], request=SamplesSerializer, **DELETE_METHOD_DOCS)
  @error_handler
  def delete(self, request, _id):
    return super().delete(self, request, _id)

class TestsMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=TestsSerializer, model=Tests)

  @extend_schema(tags=['tests'], request=TestsSerializer, **POST_METHOD_DOCS)
  @error_handler
  def post(self, request, _id):
    return super().post(self, request, _id)

  @extend_schema(tags=['tests'], request=TestsSerializer, **GET_METHOD_DOCS)
  @error_handler
  def get(self, request, _id):
    return super().get(self, request, _id)

  @extend_schema(tags=['tests'], request=TestsSerializer, **PUT_METHOD_DOCS)
  @error_handler
  def put(self, request, _id):
    return super().put(self, request, _id)

  @extend_schema(tags=['tests'], request=TestsSerializer, **DELETE_METHOD_DOCS)
  @error_handler
  def delete(self, request, _id):
    return super().delete(self, request, _id)
  
class ResultsMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=ResultsSerializer, model=Results)
  
  @extend_schema(tags=['results'], request=ResultsSerializer, **POST_METHOD_DOCS)
  @error_handler
  def post(self, request, _id):
    return super().post(self, request, _id)

  @extend_schema(tags=['results'], request=ResultsSerializer, **GET_METHOD_DOCS)
  @error_handler
  def get(self, request, _id):
    return super().get(self, request, _id)

  @extend_schema(tags=['results'], request=ResultsSerializer, **PUT_METHOD_DOCS)
  @error_handler
  def put(self, request, _id):
    return super().put(self, request, _id)

  @extend_schema(tags=['results'], request=ResultsSerializer, **DELETE_METHOD_DOCS)
  @error_handler
  def delete(self, request, _id):
    return super().delete(self, request, _id)