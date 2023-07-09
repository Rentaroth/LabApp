from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UsersSerializer, GroupsSerializer, InvitationsSerializer, ExperimentsSerializer, SamplesSerializer, TestsSerializer, ResultsSerializer
from .models import Users, Groups, Invitations, Experiments, Samples, Tests, Results
from .decorators import error_handler
from .base_methods import BaseMethods

class LoginView(APIView):
  @error_handler
  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password = password)

    if user:
      refresh = RefreshToken.for_user(user)
      return Response({'access': str(refresh.access_tokens), 'refresh': str(refresh)})
    else:
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
  