import jwt
from rest_framework.response import Response

def error_handler(func):
  def handler(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except Exception as err:
      print(str(err))
      return Response({"error": 'Something went wrong!' }, status=500)
  return handler

@error_handler
def jwt_protection(func):
  def protection(self, request):
    try:
      token = request.META.get('HTTP_AUTHORIZATION')
      validated = jwt.decode(token[7:], verify=True, algorithms=['HS256'])
      request.data['validated_token'] = validated
      return func(self, request)
    except jwt.DecodeError as err:
      print(str(err))
      print("Error al decodificar el token")
    except jwt.ExpiredSignatureError:
        print("Token JWT expirado")
    except jwt.InvalidTokenError:
        print("Token JWT inválido")
  return protection