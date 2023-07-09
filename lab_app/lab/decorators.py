from rest_framework.response import Response

def error_handler(func):
  def handler(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except Exception as err:
      return Response({"error": str(err)}, status=500)
  return handler