# Archivo de configuración de Gunicorn

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

# Nombre del módulo de la aplicación de Django y objeto de aplicación
# (debe seguir el formato "<nombre_modulo>:<nombre_objeto>")
# Por ejemplo: 'myproject.wsgi:application'
app = 'lab_app.wsgi:lab'

# Configuración adicional de Gunicorn
# ...

# Configuración de seguridad
# ...

# Configuración de rendimiento
# ...
