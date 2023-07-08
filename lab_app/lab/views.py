# from django.shortcuts import render
from django.contrib.auth import authenticate, hashers
from django.utils import timezone
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UsersSerializer
from .models import Users, Groups, Experiments, Samples, Tests, Results

class LoginView(APIView):
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
  def post(self, request):
    try:
      refresh_token = request.data['refresh_token']
      token = RefreshToken(refresh_token)
      token.blacklist()
      return Response('Log out successfully')
    except Exception as err:
      return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserCRUD(APIView):
  def post(self, request):
    try:
      request.data.update({
        'password': hashers.make_password(request.data['password']),
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
      })
      serializer = UsersSerializer(data=request.data, context={'request': request})
    except TypeError as err:
      print(err)
      return Response({ 'error': 'Password must be string type' }, status=status.HTTP_400_BAD_REQUEST)
    try:
      if serializer.is_valid():
        serializer.save()
        return Response({ 'Operation': 'Done!' }, status=status.HTTP_201_CREATED)
      else:
        return Response({ 'invalid_fields': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError as err:
      print(err)
      return Response({ 'error': 'User was not created' }, status=status.HTTP_409_CONFLICT)
    except TypeError as err:
      print(err)
      return Response({ 'error': 'User was not created' }, status=status.HTTP_400_BAD_REQUEST)
  
  def get(self, request, user_id):
    try:
      user = get_object_or_404(Users, id=user_id)
      user_dic = user.__dict__
      result = {i: j for i, j in user_dic.items() if not i.startswith('_') and not i.startswith('password')}
      return Response({'result': result}, status=status.HTTP_302_FOUND)
    except Exception as err:
      print(err)
      return Response({ 'error': 'User not found' }, status=status.HTTP_404_NOT_FOUND)
    
  def put(self, request, user_id):
    data = request.data
    if 'password' in data.keys():
      del data['password']

    try:
      Users.objects.filter(id=user_id).update(**data)
      return Response({'result': 'Done!' }, status=status.HTTP_200_OK)
    except Exception as err:
      print(err.with_traceback(err.__traceback__))
      return Response({ 'error': 'User not found' }, status=status.HTTP_404_NOT_FOUND)

  def delete(self, request, user_id):
    try:
      Users.objects.filter(id=user_id).delete()
      return Response({'result': 'Done!' }, status=status.HTTP_200_OK)
    except Exception as err:
      return Response({ 'error': 'User not found' }, status=status.HTTP_404_NOT_FOUND)