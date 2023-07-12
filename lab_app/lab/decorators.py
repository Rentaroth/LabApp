import jwt
from rest_framework.response import Response

def error_handler(func):
  def handler(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except jwt.DecodeError as err:
      print(str(err))
      print("Error on decoding token")
    except jwt.ExpiredSignatureError:
      print(str(err))
      print("Expired JWT Token")
    except jwt.InvalidTokenError:
      print(str(err))
      print("Invalid JWT Token")
    except TypeError as err:
      print(str(err))
      return Response({"error": 'Something went wrong!' }, status=500)
    except Exception as err:
      print(str(err))
      return Response({"error": 'Something went wrong!' }, status=500)
  return handler

def jwt_protection(func):
  @error_handler
  def protection(self, request, *args, **kwargs):
    token = request.META.get('HTTP_AUTHORIZATION')
    validated = jwt.decode(token[7:], verify=True, algorithms=['HS256'])
    request.data['validated_token'] = validated
    return func(self, request, *args, **kwargs)
  return protection