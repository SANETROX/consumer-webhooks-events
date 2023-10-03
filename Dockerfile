# Usa una imagen oficial de Ubuntu como imagen base
FROM ubuntu:latest

# Actualiza los paquetes del sistema
RUN apt-get update -y

# Instala Python y pip
RUN apt-get install -y python3-pip

# Establece el directorio de trabajo en el contenedor en /app
WORKDIR /app

# Agrega los contenidos del directorio actual en tu máquina al directorio /app en el contenedor
ADD . /app

# Instala los paquetes necesarios especificados en requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Ejecuta consumer.py cuando se inicia el contenedor
CMD ["python3", "consumer.py"]