import jwt
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UsersSerializer, GroupsSerializer, InvitationsSerializer, ExperimentsSerializer, SamplesSerializer, TestsSerializer, ResultsSerializer
from .models import Users, Groups, Invitations, Experiments, Samples, Tests, Results
from .decorators import error_handler, jwt_protection
from .base_methods import BaseMethods
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.conf import global_settings as settings

class LoginView(APIView):
  @error_handler
  def post(self, request):
    credentials = request.data
    serializer = UsersSerializer(data=credentials, context={'request': request}, partial=True)
    if serializer.is_valid(raise_exception=True):
      try:
        user_obj = get_object_or_404(Users, username=credentials['username'])
        user = user_obj.__dict__
        user = {i: j for i, j in user.items() if i in ['id', 'username', 'email']}
        print(user)
        user.update({
          'exp': datetime.utcnow()+timedelta(days=1)
        })
        token = jwt.encode(user, settings.SECRET_KEY,algorithm='HS256')
        return Response({'token': token}, status=status.HTTP_202_ACCEPTED)
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

class GroupsMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=GroupsSerializer, model=Groups)

class InvitationsMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=InvitationsSerializer, model=Invitations)

  @jwt_protection
  def post(self, request):
    request.data.update({
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

class ExperimentsMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=ExperimentsSerializer, model=Experiments)

class SamplesMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=SamplesSerializer, model=Samples)

class TestsMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=TestsSerializer, model=Tests)
  
class ResultsMethods(BaseMethods):
  def __init__(self):
    super().__init__(serializer=ResultsSerializer, model=Results)
  