# Usa una imagen oficial de Python como imagen base
FROM python:3.7-slim

# Establece el directorio de trabajo en el contenedor en /app
WORKDIR /app

# Agrega los contenidos del directorio actual en tu máquina al directorio /app en el contenedor
ADD . /app

# Instala los paquetes necesarios especificados en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta consumer.py cuando se inicia el contenedor
CMD ["python", "consumer.py"]