from rest_framework.response import Response

def error_handler(func):
  def handler(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except Exception as err:
      print(str(err))
      return Response({"error": 'Something went wrong!' }, status=500)
  return handler