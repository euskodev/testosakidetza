# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt y cualquier otro archivo necesario para la instalación
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . /app/

# Expone el puerto que utilizará la aplicación
EXPOSE 8000

# Define la variable de entorno necesaria para Django
ENV DJANGO_SETTINGS_MODULE=testosakidetza.settings

# Ejecuta las migraciones y el comando de arranque de Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
