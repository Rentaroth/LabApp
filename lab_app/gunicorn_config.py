# Archivo de configuración de Gunicorn
import os
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab_app.settings')
settings.configure()

def get_application():
    django_app = settings.WSGI_APPLICATION
    return django_app

# Dirección IP y puerto en el que Gunicorn escuchará las solicitudes
bind = '0.0.0.0:3000'

# Número de procesos de trabajo (workers) para manejar las solicitudes
workers = 4

# Número de hilos (threads) por proceso de trabajo
threads = 2

# Ruta al archivo de registro
errorlog = '/path/to/error.log'

# Nivel de registro para el archivo de registro
loglevel = 'info'

app = get_application()
